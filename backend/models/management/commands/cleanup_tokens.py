from django.core.management.base import BaseCommand
from django.utils import timezone

from models.tokens import AccessToken, AuthorizationCode, RefreshToken


class Command(BaseCommand):
    help = 'Purge expired authorization codes, access tokens, and refresh tokens.'

    def handle(self, *args, **options):
        now = timezone.now()

        # Delete expired or already used auth codes older than 1 hour
        codes_count, _ = AuthorizationCode.objects.filter(expires_at__lt=now).delete()
        self.stdout.write(self.style.SUCCESS(f'Removed {codes_count} expired authorization codes.'))

        # Delete expired or revoked access tokens
        tokens_count, _ = AccessToken.objects.filter(expires_at__lt=now).delete()
        self.stdout.write(self.style.SUCCESS(f'Removed {tokens_count} expired access tokens.'))

        # Delete expired refresh tokens
        refresh_count, _ = RefreshToken.objects.filter(expires_at__lt=now).delete()
        self.stdout.write(self.style.SUCCESS(f'Removed {refresh_count} expired refresh tokens.'))
