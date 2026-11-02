from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods, require_POST

from models.clients import ClientApplication
from validators.clients import ClientApplicationCreateForm, ClientApplicationUpdateForm
from .common import client_json, error, form_errors, request_data, staff_access_error


@require_http_methods(['GET', 'POST'])
def manage_clients(request):
    if request.method == 'GET':
        return list_clients(request)
    return create_client(request)


@require_http_methods(['GET', 'PATCH', 'PUT', 'DELETE'])
def manage_client(request, client_id):
    if request.method == 'GET':
        return get_client(request, client_id)
    if request.method in ('PATCH', 'PUT'):
        return update_client(request, client_id)
    return deactivate_client(request, client_id)


@require_http_methods(['GET'])
def list_clients(request):
    access_error = staff_access_error(request)
    if access_error:
        return access_error

    try:
        page_number = int(request.GET.get('page', '1'))
    except ValueError:
        return error('Page must be a positive integer.', 400)
    if page_number < 1:
        return error('Page must be a positive integer.', 400)
    page = Paginator(ClientApplication.objects.all(), 25).get_page(page_number)
    return JsonResponse({
        'count': page.paginator.count,
        'page': page.number,
        'pages': page.paginator.num_pages,
        'results': [client_json(client) for client in page.object_list],
    })


@csrf_protect
@require_POST
def create_client(request):
    access_error = staff_access_error(request)
    if access_error:
        return access_error

    data, error_response = request_data(request)
    if error_response:
        return error_response
    form = ClientApplicationCreateForm(data=data)
    unsupported_fields = set(data) - set(form.fields)
    if unsupported_fields:
        return JsonResponse({
            'errors': {'fields': [f'Unsupported fields: {", ".join(sorted(unsupported_fields))}.']},
        }, status=400)
    if not form.is_valid():
        return form_errors(form)
    client = ClientApplication.objects.create(**form.cleaned_data)
    return JsonResponse({'client': client_json(client)}, status=201)


@require_http_methods(['GET'])
def get_client(request, client_id):
    access_error = staff_access_error(request)
    if access_error:
        return access_error

    client = ClientApplication.objects.filter(client_id=client_id).first()
    if client is None:
        return error('Client application not found.', 404)
    return JsonResponse({'client': client_json(client)})


@csrf_protect
@require_http_methods(['PATCH', 'PUT'])
def update_client(request, client_id):
    access_error = staff_access_error(request)
    if access_error:
        return access_error

    client = ClientApplication.objects.filter(client_id=client_id).first()
    if client is None:
        return error('Client application not found.', 404)
    data, error_response = request_data(request)
    if error_response:
        return error_response
    unsupported_fields = set(data) - set(ClientApplicationUpdateForm.base_fields)
    if unsupported_fields:
        return JsonResponse({
            'errors': {'fields': [f'Unsupported fields: {", ".join(sorted(unsupported_fields))}.']},
        }, status=400)
    form = ClientApplicationUpdateForm(data=data)
    if not form.is_valid():
        return form_errors(form)
    for field in set(data) & set(form.fields):
        setattr(client, field, form.cleaned_data[field])
    client.save()
    return JsonResponse({'client': client_json(client)})


@csrf_protect
@require_http_methods(['DELETE'])
def deactivate_client(request, client_id):
    access_error = staff_access_error(request)
    if access_error:
        return access_error

    client = ClientApplication.objects.filter(client_id=client_id).first()
    if client is None:
        return error('Client application not found.', 404)
    client.is_active = False
    client.save(update_fields=['is_active', 'updated_at'])
    return JsonResponse({'status': 'deactivated', 'client_id': str(client.client_id)})