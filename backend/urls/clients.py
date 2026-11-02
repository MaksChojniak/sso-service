from django.urls import path

from views.clients import manage_client, manage_clients


urlpatterns = [
    path('', manage_clients, name='manage-clients'),
    path('<uuid:client_id>/', manage_client, name='manage-client'),
]