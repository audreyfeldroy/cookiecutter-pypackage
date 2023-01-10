import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn
from .models import {{ cookiecutter.model_name }}


class {{ cookiecutter.model_name }}Table(NetBoxTable):
    name = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = {{ cookiecutter.model_name }}
        fields = ('pk', 'id', 'name', 'actions')
        default_columns = ('name', 'default_action')
