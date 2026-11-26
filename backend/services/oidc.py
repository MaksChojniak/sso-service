import base64
import hashlib
import hmac
import time
import jwt
from django.conf import settings
from django.utils import timezone


def verify_pkce(code_verifier: str, code_challenge: str, method: str) -> bool:
    """Verify PKCE code_verifier against code_challenge according to RFC 7636."""
    if not code_challenge:
        return True
    if not code_verifier:
        return False

    if method == 'S256':
        digest = hashlib.sha256(code_verifier.encode('ascii')).digest()
        computed = base64.urlsafe_b64encode(digest).rstrip(b'=').decode('ascii')
        return hmac.compare_digest(computed, code_challenge)
    elif method == 'plain' or not method:
        return hmac.compare_digest(code_verifier, code_challenge)
    return False


def create_id_token(client, user, nonce='', scope='openid', issuer=None) -> str:
    """Create a signed OIDC ID Token (JWT) using client's RSA private key (RS256)."""
    now = int(time.time())
    if not issuer:
        issuer = getattr(settings, 'OIDC_ISSUER', 'http://localhost:8000')

    payload = {
        'iss': issuer,
        'sub': str(user.id),
        'aud': str(client.client_id),
        'exp': now + 3600,
        'iat': now,
        'auth_time': now,
    }

    if nonce:
        payload['nonce'] = nonce

    scopes = set(scope.split()) if isinstance(scope, str) else set(scope)

    if 'profile' in scopes:
        payload['name'] = f"{user.first_name} {user.last_name}".strip() or user.username
        payload['preferred_username'] = user.username
    if 'email' in scopes:
        payload['email'] = user.email
        payload['email_verified'] = getattr(user, 'email_verified', False)
    if 'phone' in scopes and getattr(user, 'phone_number', None):
        payload['phone_number'] = user.phone_number

    headers = {
        'kid': str(client.client_id),
        'alg': 'RS256',
    }

    token = jwt.encode(
        payload,
        client.signing_key_pem,
        algorithm='RS256',
        headers=headers,
    )
    return token


def get_user_claims(user, scope='openid') -> dict:
    """Return userinfo claims dict for the provided scopes."""
    scopes = set(scope.split()) if isinstance(scope, str) else set(scope)
    claims = {
        'sub': str(user.id),
    }

    if 'profile' in scopes:
        claims['name'] = f"{user.first_name} {user.last_name}".strip() or user.username
        claims['preferred_username'] = user.username
        if getattr(user, 'country', None):
            claims['country'] = user.country

    if 'email' in scopes:
        claims['email'] = user.email
        claims['email_verified'] = getattr(user, 'email_verified', False)

    if 'phone' in scopes and getattr(user, 'phone_number', None):
        claims['phone_number'] = user.phone_number

    return claims
