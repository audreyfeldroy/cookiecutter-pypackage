from netbox.filtersets import NetBoxModelFilterSet
from .models import {{ cookiecutter.model_name }}


class {{ cookiecutter.model_name }}FilterSet(NetBoxModelFilterSet):

    class Meta:
        model = {{ cookiecutter.model_name }}

    def search(self, queryset, name, value):
        return queryset.filter(description__icontains=value)
