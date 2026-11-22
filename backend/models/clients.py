import uuid

from django.db import models


class ClientApplication(models.Model):
    client_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=100)
    service_url = models.URLField(max_length=500)
    redirect_uris = models.JSONField(default=list)

    # Credentials — set at creation, never exposed in API responses.
    client_secret_hash = models.CharField(max_length=256)
    signing_key_pem = models.TextField()
    signing_cert_pem = models.TextField()

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name', 'id']

    def __str__(self):
        return self.name