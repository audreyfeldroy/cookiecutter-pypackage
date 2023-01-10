from django.db.models import Count

from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import {{ cookiecutter._model_name }}


class {{ cookiecutter._model_name }}ViewSet(NetBoxModelViewSet):
    queryset = models.{{ cookiecutter._model_name }}.objects.prefetch_related('tags')
    serializer_class = {{ cookiecutter._model_name }}Serializer

