import json

from django.http import JsonResponse


def error(message, status):
    return JsonResponse({'error': message}, status=status)


def staff_access_error(request):
    if not request.user.is_authenticated:
        return error('Authentication is required.', 401)
    if not request.user.is_staff:
        return error('Staff access is required.', 403)
    return None


def request_data(request):
    if request.content_type != 'application/json':
        return None, error('Content-Type must be application/json.', 415)
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None, error('Request body must contain valid JSON.', 400)
    if not isinstance(data, dict):
        return None, error('Request body must be a JSON object.', 400)
    return data, None


def form_errors(form):
    return JsonResponse({'errors': form.errors.get_json_data()}, status=400)


def client_json(client):
    return {
        'client_id': str(client.client_id),
        'name': client.name,
        'service_url': client.service_url,
        'redirect_uris': client.redirect_uris,
        'is_active': client.is_active,
        'created_at': client.created_at.isoformat(),
        'updated_at': client.updated_at.isoformat(),
    }