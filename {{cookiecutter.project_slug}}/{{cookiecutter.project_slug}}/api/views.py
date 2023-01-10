from django.db.models import Count

from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import {{ cookiecutter.__model_name }}Serializer


class {{ cookiecutter.__model_name }}ViewSet(NetBoxModelViewSet):
    queryset = models.{{ cookiecutter.__model_name }}.objects.prefetch_related('tags')
    serializer_class = {{ cookiecutter.__model_name }}Serializer

