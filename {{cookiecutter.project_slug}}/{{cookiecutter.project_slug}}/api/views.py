from django.db.models import Count

from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import {{ cookiecutter.model_name }}


class {{ cookiecutter.model_name }}ViewSet(NetBoxModelViewSet):
    queryset = models.{{ cookiecutter.model_name }}.objects.prefetch_related('tags')
    serializer_class = {{ cookiecutter.model_name }}Serializer

