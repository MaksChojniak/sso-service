import secrets
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone


class AuthorizationCode(models.Model):
    code = models.CharField(max_length=128, unique=True, default=secrets.token_urlsafe)
    client = models.ForeignKey('core.ClientApplication', on_delete=models.CASCADE, related_name='auth_codes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='auth_codes')
    redirect_uri = models.URLField(max_length=500)
    scope = models.CharField(max_length=255, default='openid')
    nonce = models.CharField(max_length=255, blank=True, default='')

    # PKCE
    code_challenge = models.CharField(max_length=128, blank=True, default='')
    code_challenge_method = models.CharField(max_length=10, blank=True, default='')

    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at

    def __str__(self):
        return f"AuthCode({self.client.name}, user={self.user.email})"


class AccessToken(models.Model):
    token = models.CharField(max_length=128, unique=True, default=secrets.token_urlsafe)
    client = models.ForeignKey('core.ClientApplication', on_delete=models.CASCADE, related_name='access_tokens')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='access_tokens')
    scope = models.CharField(max_length=255, default='openid')
    expires_at = models.DateTimeField()
    revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=1)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at

    def __str__(self):
        return f"AccessToken({self.client.name}, user={self.user.email})"


class RefreshToken(models.Model):
    token = models.CharField(max_length=128, unique=True, default=secrets.token_urlsafe)
    access_token = models.OneToOneField(AccessToken, on_delete=models.SET_NULL, null=True, blank=True, related_name='refresh_token')
    client = models.ForeignKey('core.ClientApplication', on_delete=models.CASCADE, related_name='refresh_tokens')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='refresh_tokens')
    scope = models.CharField(max_length=255, default='openid')
    expires_at = models.DateTimeField()
    revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at

    def __str__(self):
        return f"RefreshToken({self.client.name}, user={self.user.email})"


class UserConsent(models.Model):
    client = models.ForeignKey('core.ClientApplication', on_delete=models.CASCADE, related_name='consents')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='consents')
    granted_scopes = models.CharField(max_length=255, default='openid')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('client', 'user')

    def __str__(self):
        return f"Consent({self.user.email} -> {self.client.name})"


