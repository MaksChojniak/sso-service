from django.contrib.auth import get_user_model, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from validators.auth import AdminLoginForm, LoginForm, RegisterForm
from .common import error, form_errors, request_data

User = get_user_model()


def user_json(user):
    return {
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone_number': getattr(user, 'phone_number', ''),
        'country': getattr(user, 'country', ''),
        'email_verified': getattr(user, 'email_verified', False),
        'is_staff': user.is_staff,
        'is_admin_user': getattr(user, 'is_admin_user', False),
    }


@require_POST
def register_view(request):
    """POST /api/v1/auth/register"""
    data, err = request_data(request)
    if err:
        return err

    form = RegisterForm(data=data)
    if not form.is_valid():
        return form_errors(form)

    cd = form.cleaned_data
    user = User.objects.create_user(
        email=cd['email'],
        password=cd['password'],
        first_name=cd.get('first_name', ''),
        last_name=cd.get('last_name', ''),
        phone_number=cd.get('phone_number', ''),
        country=cd.get('country', ''),
    )
    login(request, user)
    return JsonResponse({'user': user_json(user)}, status=201)


@require_POST
def login_view(request):
    """POST /api/v1/auth/login"""
    data, err = request_data(request)
    if err:
        return err

    form = LoginForm(data=data)
    if not form.is_valid():
        return form_errors(form)

    user = form.cleaned_data['user']
    login(request, user)
    return JsonResponse({'user': user_json(user), 'status': 'authenticated'})


@require_POST
def admin_login_view(request):
    """POST /api/v1/admin/login"""
    data, err = request_data(request)
    if err:
        return err

    form = AdminLoginForm(data=data)
    if not form.is_valid():
        return form_errors(form)

    user = form.cleaned_data['user']
    login(request, user)
    return JsonResponse({'user': user_json(user), 'status': 'authenticated'})


@require_POST
def logout_view(request):
    """POST /api/v1/auth/logout"""
    logout(request)
    return JsonResponse({'status': 'logged_out'})


@ensure_csrf_cookie
@require_GET
def session_me_view(request):
    """GET /api/v1/auth/me"""
    if not request.user.is_authenticated:
        return JsonResponse({'authenticated': False}, status=200)
    return JsonResponse({
        'authenticated': True,
        'user': user_json(request.user),
    })
