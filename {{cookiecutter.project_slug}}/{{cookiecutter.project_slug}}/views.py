from django.db.models import Count

from netbox.views import generic
from . import filtersets, forms, models, tables


#
# AccessList views
#

class AccessListView(generic.ObjectView):
    queryset = models.AccessList.objects.all()

    def get_extra_context(self, request, instance):
        table = tables.AccessListRuleTable(instance.rules.all())
        table.configure(request)

        return {
            'rules_table': table,
        }


class AccessListListView(generic.ObjectListView):
    queryset = models.AccessList.objects.annotate(
        rule_count=Count('rules')
    )
    table = tables.AccessListTable


class AccessListEditView(generic.ObjectEditView):
    queryset = models.AccessList.objects.all()
    form = forms.AccessListForm


class AccessListDeleteView(generic.ObjectDeleteView):
    queryset = models.AccessList.objects.all()


#
# AccessListRule views
#

class AccessListRuleView(generic.ObjectView):
    queryset = models.AccessListRule.objects.all()


class AccessListRuleListView(generic.ObjectListView):
    queryset = models.AccessListRule.objects.all()
    table = tables.AccessListRuleTable
    filterset = filtersets.AccessListRuleFilterSet
    filterset_form = forms.AccessListRuleFilterForm


class AccessListRuleEditView(generic.ObjectEditView):
    queryset = models.AccessListRule.objects.all()
    form = forms.AccessListRuleForm


class AccessListRuleDeleteView(generic.ObjectDeleteView):
    queryset = models.AccessListRule.objects.all()
