import datetime
import json
import uuid

from django.apps import apps
from django.http import JsonResponse
from django.utils.text import capfirst
from django.views.decorators.http import require_GET

from .common import error, staff_access_error

EXCLUDED_FIELDS = frozenset({
    'password',
    'client_secret_hash',
    'signing_key_pem',
    'signing_cert_pem',
})

MASKED_FIELDS = frozenset({
    'token',
    'code',
})


def _mask_value(value):
    text = str(value)
    if not text:
        return ''
    if len(text) <= 12:
        return '••••'
    return f'{text[:8]}…{text[-4:]}'


def _get_core_models():
    return {
        model._meta.model_name: model
        for model in apps.get_app_config('core').get_models()
    }


def _get_visible_fields(model):
    return [
        field for field in model._meta.fields
        if field.name not in EXCLUDED_FIELDS
    ]


def _serialize_field_value(obj, field):
    if field.is_relation:
        related = getattr(obj, field.name, None)
        return str(related) if related is not None else None

    value = getattr(obj, field.name, None)
    if value is None:
        return None
    if field.name in MASKED_FIELDS:
        return _mask_value(value)
    if isinstance(value, (datetime.datetime, datetime.date)):
        return value.isoformat()
    if isinstance(value, uuid.UUID):
        return str(value)
    if isinstance(value, (list, dict)):
        return json.dumps(value)
    return value


def _serialize_instance(obj, fields):
    return {
        field.name: _serialize_field_value(obj, field)
        for field in fields
    }


@require_GET
def list_database_models(request):
    """GET /api/v1/admin/database/models"""
    err = staff_access_error(request)
    if err:
        return err

    models_data = [
        {
            'key': key,
            'label': model.__name__,
            'count': model.objects.count(),
        }
        for key, model in _get_core_models().items()
    ]
    return JsonResponse({'models': models_data})


@require_GET
def get_database_model_rows(request, model_key):
    """GET /api/v1/admin/database/models/<model_key>"""
    err = staff_access_error(request)
    if err:
        return err

    model = _get_core_models().get(model_key)
    if not model:
        return error('Model not found.', 404)

    try:
        limit = min(max(int(request.GET.get('limit', 100)), 1), 250)
    except ValueError:
        limit = 100
    try:
        offset = max(int(request.GET.get('offset', 0)), 0)
    except ValueError:
        offset = 0

    fields = _get_visible_fields(model)
    columns = [
        {'key': field.name, 'label': capfirst(str(field.verbose_name))}
        for field in fields
    ]

    queryset = model.objects.all()
    fk_fields = [field.name for field in fields if field.is_relation]
    if fk_fields:
        queryset = queryset.select_related(*fk_fields)

    total_count = queryset.count()
    rows = [_serialize_instance(obj, fields) for obj in queryset[offset : offset + limit]]

    return JsonResponse({
        'model': {
            'key': model_key,
            'label': model.__name__,
        },
        'columns': columns,
        'rows': rows,
        'total_count': total_count,
    })
