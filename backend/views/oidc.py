import base64
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from models.clients import ClientApplication
from models.tokens import AccessToken, AuthorizationCode, RefreshToken
from services.crypto import public_key_to_jwk, verify_client_secret
from services.oidc import create_id_token, get_user_claims, verify_pkce
from .common import error


def get_issuer(request) -> str:
    default_issuer = getattr(settings, 'OIDC_ISSUER', None)
    if default_issuer:
        return default_issuer
    return request.build_absolute_uri('/')[:-1]


@require_GET
def openid_configuration(request):
    """OIDC Discovery Endpoint: /.well-known/openid-configuration"""
    issuer = get_issuer(request)
    return JsonResponse({
        'issuer': issuer,
        'authorization_endpoint': f"{issuer}/oidc/authorize",
        'token_endpoint': f"{issuer}/oidc/token",
        'userinfo_endpoint': f"{issuer}/oidc/userinfo",
        'jwks_uri': f"{issuer}/oidc/.well-known/jwks.json",
        'response_types_supported': ['code'],
        'subject_types_supported': ['public'],
        'id_token_signing_alg_values_supported': ['RS256'],
        'scopes_supported': ['openid', 'profile', 'email', 'phone'],
        'token_endpoint_auth_methods_supported': ['client_secret_basic', 'client_secret_post'],
        'claims_supported': ['sub', 'iss', 'aud', 'exp', 'iat', 'name', 'preferred_username', 'email', 'email_verified', 'phone_number', 'country'],
        'code_challenge_methods_supported': ['S256', 'plain'],
    })


@require_GET
def jwks(request):
    """OIDC JWKS Endpoint: /oidc/.well-known/jwks.json"""
    client_id = request.GET.get('client_id')
    keys = []

    if client_id:
        clients = ClientApplication.objects.filter(client_id=client_id, is_active=True)
    else:
        clients = ClientApplication.objects.filter(is_active=True)

    for c in clients:
        if c.signing_key_pem:
            keys.append(public_key_to_jwk(c.signing_key_pem, kid=str(c.client_id)))

    return JsonResponse({'keys': keys})


@require_http_methods(['GET', 'POST'])
def authorize(request):
    """OIDC Authorization Endpoint: /oidc/authorize"""
    client_id = request.GET.get('client_id') or request.POST.get('client_id')
    redirect_uri = request.GET.get('redirect_uri') or request.POST.get('redirect_uri')
    response_type = request.GET.get('response_type') or request.POST.get('response_type')
    scope = request.GET.get('scope', 'openid') or request.POST.get('scope', 'openid')
    state = request.GET.get('state', '') or request.POST.get('state', '')
    nonce = request.GET.get('nonce', '') or request.POST.get('nonce', '')
    code_challenge = request.GET.get('code_challenge', '') or request.POST.get('code_challenge', '')
    code_challenge_method = request.GET.get('code_challenge_method', '') or request.POST.get('code_challenge_method', '')

    if not client_id or not redirect_uri:
        return error('Missing required parameters: client_id and redirect_uri', 400)

    try:
        client = ClientApplication.objects.get(client_id=client_id, is_active=True)
    except (ClientApplication.DoesNotExist, ValueError):
        return error('Invalid client_id', 400)

    if redirect_uri not in client.redirect_uris:
        return error('Mismatching redirect_uri', 400)

    if response_type != 'code':
        query = urlencode({'error': 'unsupported_response_type', 'state': state})
        return HttpResponseRedirect(f"{redirect_uri}?{query}")

    # Check user authentication
    if not request.user.is_authenticated:
        # Redirect to frontend login page with return url
        login_url = getattr(settings, 'SSO_LOGIN_URL', '/login')
        params = urlencode({
            'next': request.get_full_path(),
            'client_id': client_id,
            'client_name': client.name,
        })
        return HttpResponseRedirect(f"{login_url}?{params}")

    # User is authenticated -> create authorization code
    auth_code = AuthorizationCode.objects.create(
        client=client,
        user=request.user,
        redirect_uri=redirect_uri,
        scope=scope,
        nonce=nonce,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
    )

    query_params = {'code': auth_code.code}
    if state:
        query_params['state'] = state

    return HttpResponseRedirect(f"{redirect_uri}?{urlencode(query_params)}")


@csrf_exempt
@require_POST
def token(request):
    """OIDC Token Endpoint: /oidc/token"""
    grant_type = request.POST.get('grant_type')

    # Authenticate client: Basic Auth or POST body
    client_id = request.POST.get('client_id')
    client_secret = request.POST.get('client_secret')

    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Basic '):
        try:
            credentials = base64.b64decode(auth_header[6:]).decode('utf-8').split(':', 1)
            if len(credentials) == 2:
                client_id, client_secret = credentials
        except Exception:
            return JsonResponse({'error': 'invalid_client', 'error_description': 'Malformed authorization header'}, status=401)

    if not client_id:
        return JsonResponse({'error': 'invalid_client', 'error_description': 'Missing client_id'}, status=401)

    try:
        client = ClientApplication.objects.get(client_id=client_id, is_active=True)
    except (ClientApplication.DoesNotExist, ValueError):
        return JsonResponse({'error': 'invalid_client', 'error_description': 'Unknown client'}, status=401)

    if not client_secret or not verify_client_secret(client_secret, client.client_secret_hash):
        return JsonResponse({'error': 'invalid_client', 'error_description': 'Invalid client_secret'}, status=401)

    issuer = get_issuer(request)

    if grant_type == 'authorization_code':
        code_val = request.POST.get('code')
        redirect_uri = request.POST.get('redirect_uri')
        code_verifier = request.POST.get('code_verifier', '')

        if not code_val:
            return JsonResponse({'error': 'invalid_request', 'error_description': 'Missing code'}, status=400)

        try:
            auth_code = AuthorizationCode.objects.get(code=code_val, client=client)
        except AuthorizationCode.DoesNotExist:
            return JsonResponse({'error': 'invalid_grant', 'error_description': 'Invalid authorization code'}, status=400)

        if auth_code.is_used:
            return JsonResponse({'error': 'invalid_grant', 'error_description': 'Authorization code already used'}, status=400)

        if auth_code.is_expired:
            return JsonResponse({'error': 'invalid_grant', 'error_description': 'Authorization code expired'}, status=400)

        if redirect_uri and auth_code.redirect_uri != redirect_uri:
            return JsonResponse({'error': 'invalid_grant', 'error_description': 'Redirect URI mismatch'}, status=400)

        # Check PKCE if required
        if auth_code.code_challenge:
            if not verify_pkce(code_verifier, auth_code.code_challenge, auth_code.code_challenge_method):
                return JsonResponse({'error': 'invalid_grant', 'error_description': 'PKCE verification failed'}, status=400)

        # Mark code as used
        auth_code.is_used = True
        auth_code.save(update_fields=['is_used'])

        access_token = AccessToken.objects.create(
            client=client,
            user=auth_code.user,
            scope=auth_code.scope,
        )

        refresh_token = RefreshToken.objects.create(
            access_token=access_token,
            client=client,
            user=auth_code.user,
            scope=auth_code.scope,
        )

        id_token = create_id_token(
            client=client,
            user=auth_code.user,
            nonce=auth_code.nonce,
            scope=auth_code.scope,
            issuer=issuer,
        )

        return JsonResponse({
            'access_token': access_token.token,
            'token_type': 'Bearer',
            'expires_in': 3600,
            'refresh_token': refresh_token.token,
            'id_token': id_token,
            'scope': auth_code.scope,
        })

    elif grant_type == 'refresh_token':
        refresh_token_val = request.POST.get('refresh_token')
        if not refresh_token_val:
            return JsonResponse({'error': 'invalid_request', 'error_description': 'Missing refresh_token'}, status=400)

        try:
            rt = RefreshToken.objects.get(token=refresh_token_val, client=client)
        except RefreshToken.DoesNotExist:
            return JsonResponse({'error': 'invalid_grant', 'error_description': 'Invalid refresh token'}, status=400)

        if rt.revoked or rt.is_expired:
            return JsonResponse({'error': 'invalid_grant', 'error_description': 'Refresh token expired or revoked'}, status=400)

        new_access_token = AccessToken.objects.create(
            client=client,
            user=rt.user,
            scope=rt.scope,
        )

        id_token = create_id_token(
            client=client,
            user=rt.user,
            scope=rt.scope,
            issuer=issuer,
        )

        return JsonResponse({
            'access_token': new_access_token.token,
            'token_type': 'Bearer',
            'expires_in': 3600,
            'id_token': id_token,
            'scope': rt.scope,
        })

    return JsonResponse({'error': 'unsupported_grant_type'}, status=400)


@require_GET
def userinfo(request):
    """OIDC UserInfo Endpoint: /oidc/userinfo"""
    auth_header = request.headers.get('Authorization', '')
    token_str = None
    if auth_header.startswith('Bearer '):
        token_str = auth_header[7:].strip()

    if not token_str:
        return JsonResponse({'error': 'invalid_token', 'error_description': 'Missing access token'}, status=401)

    try:
        at = AccessToken.objects.select_related('user').get(token=token_str)
    except AccessToken.DoesNotExist:
        return JsonResponse({'error': 'invalid_token', 'error_description': 'Invalid access token'}, status=401)

    if at.revoked or at.is_expired:
        return JsonResponse({'error': 'invalid_token', 'error_description': 'Access token expired or revoked'}, status=401)

    claims = get_user_claims(at.user, scope=at.scope)
    return JsonResponse(claims)
