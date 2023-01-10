from django.urls import path

from netbox.views.generic import ObjectChangeLogView
from . import models, views


urlpatterns = (

    # Access lists
    path('{{ cookiecutter.__model_url }}s/', views.{{ cookiecutter.__model_name }}ListView.as_view(), name='{{ cookiecutter.__model_url_name }}_list'),
    path('{{ cookiecutter.__model_url }}s/add/', views.{{ cookiecutter.__model_name }}EditView.as_view(), name='{{ cookiecutter.__model_url_name }}_add'),
    path('{{ cookiecutter.__model_url }}s/<int:pk>/', views.{{ cookiecutter.__model_name }}View.as_view(), name='{{ cookiecutter.__model_url_name }}'),
    path('{{ cookiecutter.__model_url }}s/<int:pk>/edit/', views.{{ cookiecutter.__model_name }}EditView.as_view(), name='{{ cookiecutter.__model_url_name }}_edit'),
    path('{{ cookiecutter.__model_url }}s/<int:pk>/delete/', views.{{ cookiecutter.__model_name }}DeleteView.as_view(), name='{{ cookiecutter.__model_url_name }}_delete'),
    path('{{ cookiecutter.__model_url }}s/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='{{ cookiecutter.__model_url_name }}_changelog', kwargs={
        'model': models.{{ cookiecutter.__model_name }}
    }),

)
