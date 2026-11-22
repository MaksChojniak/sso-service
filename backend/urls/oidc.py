from django.urls import path

from views.oidc import authorize, jwks, openid_configuration, token, userinfo

urlpatterns = [
    path('authorize', authorize, name='oidc-authorize'),
    path('token', token, name='oidc-token'),
    path('userinfo', userinfo, name='oidc-userinfo'),
    path('.well-known/jwks.json', jwks, name='oidc-jwks'),
]
