from django.urls import path

from views.auth import (
    admin_login_view, login_view, logout_view, register_view, session_me_view,
)

urlpatterns = [
    path('register', register_view, name='auth-register'),
    path('login', login_view, name='auth-login'),
    path('logout', logout_view, name='auth-logout'),
    path('me', session_me_view, name='auth-me'),
]
