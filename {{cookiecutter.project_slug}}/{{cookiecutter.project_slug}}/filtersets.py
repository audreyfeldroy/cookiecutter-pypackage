from netbox.filtersets import NetBoxModelFilterSet
from .models import {{ cookiecutter._model_name }}


class {{ cookiecutter._model_name }}FilterSet(NetBoxModelFilterSet):

    class Meta:
        model = {{ cookiecutter._model_name }}

    def search(self, queryset, name, value):
        return queryset.filter(description__icontains=value)
