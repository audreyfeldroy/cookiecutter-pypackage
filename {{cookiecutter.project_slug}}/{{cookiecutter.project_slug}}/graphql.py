from graphene import ObjectType
from netbox.graphql.types import NetBoxObjectType
from netbox.graphql.fields import ObjectField, ObjectListField
from . import filtersets, models


#
# Object types
#

class AccessListType(NetBoxObjectType):

    class Meta:
        model = models.AccessList
        fields = '__all__'


class AccessListRuleType(NetBoxObjectType):

    class Meta:
        model = models.AccessListRule
        fields = '__all__'
        filterset_class = filtersets.AccessListRuleFilterSet


#
# Queries
#

class Query(ObjectType):
    access_list = ObjectField(AccessListType)
    access_list_list = ObjectListField(AccessListType)

    access_list_rule = ObjectField(AccessListRuleType)
    access_list_rule_list = ObjectListField(AccessListRuleType)


schema = Query
