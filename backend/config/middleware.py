import os
import time
from django.core.cache import cache
from django.http import JsonResponse


class SimpleRateLimitMiddleware:
    """Basic IP-based rate limiting middleware for sensitive auth endpoints."""

    # endpoints to rate limit: endpoint_prefix -> (max_requests, window_seconds)
    RATE_LIMITS = {
        '/api/v1/auth/login': (10, 60),
        '/api/v1/auth/register': (5, 60),
        '/api/v1/admin/login': (5, 60),
        '/oidc/token': (30, 60),
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if request.method == 'POST':
            for endpoint, (max_req, window) in self.RATE_LIMITS.items():
                if path.startswith(endpoint):
                    ip = self._get_client_ip(request)
                    cache_key = f'ratelimit:{ip}:{endpoint}'
                    current_count = cache.get(cache_key, 0)

                    if current_count >= max_req:
                        return JsonResponse({
                            'error': 'too_many_requests',
                            'message': 'Too many requests. Please slow down and try again later.',
                        }, status=429)

                    if current_count == 0:
                        cache.set(cache_key, 1, timeout=window)
                    else:
                        try:
                            cache.incr(cache_key)
                        except Exception:
                            cache.set(cache_key, current_count + 1, timeout=window)
                    break

        return self.get_response(request)

    def _get_client_ip(self, request):
        remote_addr = request.META.get('REMOTE_ADDR', '')
        trusted_proxies = {
            ip.strip()
            for ip in os.environ.get('TRUSTED_PROXY_IPS', '127.0.0.1,::1').split(',')
            if ip.strip()
        }
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for and remote_addr in trusted_proxies:
            return x_forwarded_for.split(',')[0].strip()
        return remote_addr
