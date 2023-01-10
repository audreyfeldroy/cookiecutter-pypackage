from django.urls import path

from netbox.views.generic import ObjectChangeLogView
from . import models, views


urlpatterns = (

    # Access lists
    path('{{ cookiecutter._model_url }}s/', views.{{ cookiecutter._model_name }}ListView.as_view(), name='{{ cookiecutter._model_url_name }}_list'),
    path('{{ cookiecutter._model_url }}s/add/', views.{{ cookiecutter._model_name }}EditView.as_view(), name='{{ cookiecutter._model_url_name }}_add'),
    path('{{ cookiecutter._model_url }}s/<int:pk>/', views.{{ cookiecutter._model_name }}View.as_view(), name='{{ cookiecutter._model_url_name }}'),
    path('{{ cookiecutter._model_url }}s/<int:pk>/edit/', views.{{ cookiecutter._model_name }}EditView.as_view(), name='{{ cookiecutter._model_url_name }}_edit'),
    path('{{ cookiecutter._model_url }}s/<int:pk>/delete/', views.{{ cookiecutter._model_name }}DeleteView.as_view(), name='{{ cookiecutter._model_url_name }}_delete'),
    path('{{ cookiecutter._model_url }}s/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='{{ cookiecutter._model_url_name }}_changelog', kwargs={
        'model': models.{{ cookiecutter._model_name }}
    }),

)
