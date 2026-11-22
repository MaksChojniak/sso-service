import base64
import hashlib
from urllib.parse import parse_qs, urlparse

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from models.clients import ClientApplication
from models.tokens import AccessToken, AuthorizationCode
from services.crypto import (
    generate_client_secret, generate_rsa_keypair, generate_self_signed_cert,
    hash_client_secret, private_key_to_pem,
)


User = get_user_model()


class OIDCFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='alice@example.com',
            username='alice',
            password='Password123!',
            first_name='Alice',
            last_name='Smith',
        )
        self.plain_secret = generate_client_secret()
        self.key = generate_rsa_keypair()
        self.client_app = ClientApplication.objects.create(
            name='Test App',
            service_url='https://app.example.com',
            redirect_uris=['https://app.example.com/callback'],
            client_secret_hash=hash_client_secret(self.plain_secret),
            signing_key_pem=private_key_to_pem(self.key),
            signing_cert_pem=generate_self_signed_cert(self.key, 'Test App'),
        )

    def test_discovery_and_jwks(self):
        disc_res = self.client.get(reverse('oidc-discovery'))
        self.assertEqual(disc_res.status_code, 200)
        self.assertIn('authorization_endpoint', disc_res.json())

        jwks_res = self.client.get(reverse('oidc-jwks'))
        self.assertEqual(jwks_res.status_code, 200)
        keys = jwks_res.json().get('keys', [])
        self.assertGreaterEqual(len(keys), 1)
        self.assertEqual(keys[0]['kid'], str(self.client_app.client_id))

    def test_full_oidc_authorization_code_flow_with_pkce(self):
        # 1. Prepare PKCE
        verifier = 'dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk'
        digest = hashlib.sha256(verifier.encode('ascii')).digest()
        challenge = base64.urlsafe_b64encode(digest).rstrip(b'=').decode('ascii')

        # 2. Authorize while logged in
        self.client.force_login(self.user)
        auth_url = reverse('oidc-authorize')
        response = self.client.get(auth_url, {
            'client_id': str(self.client_app.client_id),
            'redirect_uri': 'https://app.example.com/callback',
            'response_type': 'code',
            'scope': 'openid profile email',
            'state': 'xyz123',
            'code_challenge': challenge,
            'code_challenge_method': 'S256',
        })

        self.assertEqual(response.status_code, 302)
        parsed = urlparse(response.url)
        params = parse_qs(parsed.query)
        self.assertIn('code', params)
        self.assertEqual(params['state'][0], 'xyz123')
        code = params['code'][0]

        # 3. Exchange code at /oidc/token
        token_url = reverse('oidc-token')
        token_res = self.client.post(token_url, {
            'grant_type': 'authorization_code',
            'client_id': str(self.client_app.client_id),
            'client_secret': self.plain_secret,
            'code': code,
            'redirect_uri': 'https://app.example.com/callback',
            'code_verifier': verifier,
        })
        self.assertEqual(token_res.status_code, 200)
        tokens = token_res.json()
        self.assertIn('access_token', tokens)
        self.assertIn('id_token', tokens)
        self.assertIn('refresh_token', tokens)

        # 4. Access /oidc/userinfo with AccessToken
        userinfo_url = reverse('oidc-userinfo')
        uinfo_res = self.client.get(
            userinfo_url,
            HTTP_AUTHORIZATION=f"Bearer {tokens['access_token']}"
        )
        self.assertEqual(uinfo_res.status_code, 200)
        claims = uinfo_res.json()
        self.assertEqual(claims['email'], 'alice@example.com')
        self.assertEqual(claims['name'], 'Alice Smith')

    def test_unauthenticated_authorize_redirects_to_login(self):
        auth_url = reverse('oidc-authorize')
        response = self.client.get(auth_url, {
            'client_id': str(self.client_app.client_id),
            'redirect_uri': 'https://app.example.com/callback',
            'response_type': 'code',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login'))
