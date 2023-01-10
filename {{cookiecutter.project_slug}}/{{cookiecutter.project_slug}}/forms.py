from django import forms

from ipam.models import Prefix
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from .models import {{ cookiecutter.__model_name }}


class {{ cookiecutter.__model_name }}Form(NetBoxModelForm):

    class Meta:
        model = {{ cookiecutter.__model_name }}
        fields = ('name', 'tags')
