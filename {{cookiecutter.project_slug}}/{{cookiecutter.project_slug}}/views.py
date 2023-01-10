from django.db.models import Count

from netbox.views import generic
from . import filtersets, forms, models, tables


#
# AccessList views
#

class {{ cookiecutter._model_name }}View(generic.ObjectView):
    queryset = models.{{ cookiecutter._model_name }}.objects.all()


class {{ cookiecutter._model_name }}ListView(generic.ObjectListView):
    queryset = models.{{ cookiecutter._model_name }}
    table = tables.{{ cookiecutter._model_name }}Table


class {{ cookiecutter._model_name }}EditView(generic.ObjectEditView):
    queryset = models.{{ cookiecutter._model_name }}.objects.all()
    form = forms.{{ cookiecutter._model_name }}Form


class {{ cookiecutter._model_name }}DeleteView(generic.ObjectDeleteView):
    queryset = models.{{ cookiecutter._model_name }}.objects.all()


