import base64
import datetime
import secrets

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from django.contrib.auth.hashers import check_password, make_password


# ---------------------------------------------------------------------------
# Client secret
# ---------------------------------------------------------------------------

def generate_client_secret(length=48):
    """Return a cryptographically random URL-safe client secret."""
    return secrets.token_urlsafe(length)


def hash_client_secret(secret):
    """Hash *secret* with Django's default password hasher (PBKDF2)."""
    return make_password(secret)


def verify_client_secret(secret, hashed):
    """Verify *secret* against a previously hashed value."""
    return check_password(secret, hashed)


# ---------------------------------------------------------------------------
# RSA key pair
# ---------------------------------------------------------------------------

def generate_rsa_keypair(key_size=2048):
    """Generate and return an RSA private key object."""
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )


def private_key_to_pem(private_key):
    """Serialize an RSA private key to PEM (unencrypted)."""
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode('utf-8')


def load_private_key(pem):
    """Deserialize a PEM-encoded private key."""
    return serialization.load_pem_private_key(pem.encode('utf-8'), password=None)


# ---------------------------------------------------------------------------
# Self-signed X.509 certificate
# ---------------------------------------------------------------------------

def generate_self_signed_cert(private_key, common_name, days_valid=3650):
    """Create a self-signed X.509 certificate for *common_name*.

    The certificate is valid for *days_valid* days (default 10 years) and
    allows ``digitalSignature`` usage only.
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + datetime.timedelta(days=days_valid))
        .add_extension(
            x509.BasicConstraints(ca=False, path_length=None),
            critical=True,
        )
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_encipherment=False,
                content_commitment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=False,
                crl_sign=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .sign(private_key, hashes.SHA256())
    )
    return cert.public_bytes(serialization.Encoding.PEM).decode('utf-8')


# ---------------------------------------------------------------------------
# JWK helpers (for the JWKS endpoint in later stages)
# ---------------------------------------------------------------------------

def _int_to_base64url(value, length):
    """Encode a positive integer as an unpadded Base64url string."""
    raw = value.to_bytes(length, byteorder='big')
    return base64.urlsafe_b64encode(raw).rstrip(b'=').decode('ascii')


def public_key_to_jwk(private_key_pem, kid=None):
    """Derive a JWK (public) dict from a PEM-encoded private key.

    The returned dict is suitable for inclusion in a JWKS ``keys`` array.
    """
    public_key = load_private_key(private_key_pem).public_key()
    numbers = public_key.public_numbers()
    key_size_bytes = (public_key.key_size + 7) // 8
    jwk = {
        'kty': 'RSA',
        'use': 'sig',
        'alg': 'RS256',
        'n': _int_to_base64url(numbers.n, key_size_bytes),
        'e': _int_to_base64url(numbers.e, 3),
    }
    if kid:
        jwk['kid'] = kid
    return jwk
