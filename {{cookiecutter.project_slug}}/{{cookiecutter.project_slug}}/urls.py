from django.urls import path

from netbox.views.generic import ObjectChangeLogView
from . import models, views


urlpatterns = (

    # Access lists
    path('{{ cookiecutter.model_url }}s/', views.{{ cookiecutter.model_name }}ListView.as_view(), name='{{ cookiecutter.model_url_name }}_list'),
    path('{{ cookiecutter.model_url }}s/add/', views.{{ cookiecutter.model_name }}EditView.as_view(), name='{{ cookiecutter.model_url_name }}_add'),
    path('{{ cookiecutter.model_url }}s/<int:pk>/', views.{{ cookiecutter.model_name }}View.as_view(), name='{{ cookiecutter.model_url_name }}'),
    path('{{ cookiecutter.model_url }}s/<int:pk>/edit/', views.{{ cookiecutter.model_name }}EditView.as_view(), name='{{ cookiecutter.model_url_name }}_edit'),
    path('{{ cookiecutter.model_url }}s/<int:pk>/delete/', views.{{ cookiecutter.model_name }}DeleteView.as_view(), name='{{ cookiecutter.model_url_name }}_delete'),
    path('{{ cookiecutter.model_url }}s/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='{{ cookiecutter.model_url_name }}_changelog', kwargs={
        'model': models.{{ cookiecutter.model_name }}
    }),

)
