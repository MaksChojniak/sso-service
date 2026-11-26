from django.urls import path

from views.database import get_database_model_rows, list_database_models


urlpatterns = [
    path('models', list_database_models, name='admin-database-models'),
    path('models/<str:model_key>', get_database_model_rows, name='admin-database-model-rows'),
]
