from django.db.models import Count

from netbox.views import generic
from . import filtersets, forms, models, tables


#
# AccessList views
#

class {{ cookiecutter.__model_name }}View(generic.ObjectView):
    queryset = models.{{ cookiecutter.__model_name }}.objects.all()


class {{ cookiecutter.__model_name }}ListView(generic.ObjectListView):
    queryset = models.{{ cookiecutter.__model_name }}
    table = tables.{{ cookiecutter.__model_name }}Table


class {{ cookiecutter.__model_name }}EditView(generic.ObjectEditView):
    queryset = models.{{ cookiecutter.__model_name }}.objects.all()
    form = forms.{{ cookiecutter.__model_name }}Form


class {{ cookiecutter.__model_name }}DeleteView(generic.ObjectDeleteView):
    queryset = models.{{ cookiecutter.__model_name }}.objects.all()


