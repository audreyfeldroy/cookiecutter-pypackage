from netbox.api.routers import NetBoxRouter
from . import views


app_name = '{{ cookiecutter.project_slug }}'

router = NetBoxRouter()
router.register('access-lists', views.{{ cookiecutter.__model_name }}ViewSet)

urlpatterns = router.urls
