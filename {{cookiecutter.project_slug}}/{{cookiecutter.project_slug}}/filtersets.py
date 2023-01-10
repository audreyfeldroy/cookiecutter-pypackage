from netbox.filtersets import NetBoxModelFilterSet
from .models import {{ cookiecutter.__model_name }}


class {{ cookiecutter.__model_name }}FilterSet(NetBoxModelFilterSet):

    class Meta:
        model = {{ cookiecutter.__model_name }}
        fields = ['name', ]

    def search(self, queryset, name, value):
        return queryset.filter(description__icontains=value)
