from django.urls import path

from views.clients import (
    manage_client, manage_clients, overview_stats,
    rotate_client_keys, rotate_client_secret,
)


urlpatterns = [
    path('', manage_clients, name='manage-clients'),
    path('stats/overview', overview_stats, name='admin-overview-stats'),
    path('<uuid:client_id>/', manage_client, name='manage-client'),
    path('<uuid:client_id>/rotate-secret', rotate_client_secret, name='client-rotate-secret'),
    path('<uuid:client_id>/rotate-keys', rotate_client_keys, name='client-rotate-keys'),
]
