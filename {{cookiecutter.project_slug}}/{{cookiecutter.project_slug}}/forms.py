from django import forms

from ipam.models import Prefix
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from .models import AccessList, AccessListRule, ActionChoices, ProtocolChoices


class AccessListForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = AccessList
        fields = ('name', 'default_action', 'comments', 'tags')


class AccessListRuleForm(NetBoxModelForm):
    access_list = DynamicModelChoiceField(
        queryset=AccessList.objects.all()
    )
    source_prefix = DynamicModelChoiceField(
        queryset=Prefix.objects.all()
    )
    destination_prefix = DynamicModelChoiceField(
        queryset=Prefix.objects.all()
    )

    class Meta:
        model = AccessListRule
        fields = (
            'access_list', 'index', 'description', 'source_prefix', 'source_ports', 'destination_prefix',
            'destination_ports', 'protocol', 'action', 'tags',
        )


class AccessListRuleFilterForm(NetBoxModelFilterSetForm):
    model = AccessListRule
    access_list = forms.ModelMultipleChoiceField(
        queryset=AccessList.objects.all(),
        required=False
    )
    index = forms.IntegerField(
        required=False
    )
    protocol = forms.MultipleChoiceField(
        choices=ProtocolChoices,
        required=False
    )
    action = forms.MultipleChoiceField(
        choices=ActionChoices,
        required=False
    )
