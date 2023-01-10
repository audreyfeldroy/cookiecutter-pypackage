from django.db.models import Count

from netbox.views import generic
from . import filtersets, forms, models, tables


#
# AccessList views
#

class {{ cookiecutter.model_name }}View(generic.ObjectView):
    queryset = models.{{ cookiecutter.model_name }}.objects.all()


class {{ cookiecutter.model_name }}ListView(generic.ObjectListView):
    queryset = models.{{ cookiecutter.model_name }}
    table = tables.{{ cookiecutter.model_name }}Table


class {{ cookiecutter.model_name }}EditView(generic.ObjectEditView):
    queryset = models.{{ cookiecutter.model_name }}.objects.all()
    form = forms.{{ cookiecutter.model_name }}Form


class {{ cookiecutter.model_name }}DeleteView(generic.ObjectDeleteView):
    queryset = models.{{ cookiecutter.model_name }}.objects.all()


