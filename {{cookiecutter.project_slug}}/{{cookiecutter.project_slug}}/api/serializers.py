from rest_framework import serializers

from ipam.api.serializers import NestedPrefixSerializer
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import {{ cookiecutter.model_name }}


#
# Nested serializers
#

class Nested{{ cookiecutter.model_name }}Serializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_access_lists-api:accesslist-detail'
    )

    class Meta:
        model = AccessList
        fields = ('id', 'url', 'display', 'name')



#
# Regular serializers
#

class {{ cookiecutter.model_name }}Serializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_access_lists-api:accesslist-detail'
    )
    rule_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = AccessList
        fields = (
            'id', 'url', 'display', 'name', 'default_action', 'comments', 'tags', 'custom_fields', 'created',
            'last_updated', 'rule_count',
        )
