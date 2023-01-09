from rest_framework import serializers

from ipam.api.serializers import NestedPrefixSerializer
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import AccessList, AccessListRule


#
# Nested serializers
#

class NestedAccessListSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_access_lists-api:accesslist-detail'
    )

    class Meta:
        model = AccessList
        fields = ('id', 'url', 'display', 'name')


class NestedAccessListRuleSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_access_lists-api:accesslistrule-detail'
    )

    class Meta:
        model = AccessListRule
        fields = ('id', 'url', 'display', 'index')


#
# Regular serializers
#

class AccessListSerializer(NetBoxModelSerializer):
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


class AccessListRuleSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_access_lists-api:accesslistrule-detail'
    )
    access_list = NestedAccessListSerializer()
    source_prefix = NestedPrefixSerializer()
    destination_prefix = NestedPrefixSerializer()

    class Meta:
        model = AccessListRule
        fields = (
            'id', 'url', 'display', 'access_list', 'index', 'protocol', 'source_prefix', 'source_ports',
            'destination_prefix', 'destination_ports', 'action', 'tags', 'custom_fields', 'created',
            'last_updated',
        )
