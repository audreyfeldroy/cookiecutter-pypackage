"""Top-level package for {{ cookiecutter.project_name }}."""

__author__ = """{{ cookiecutter.full_name }}"""
__email__ = '{{ cookiecutter.email }}'
__version__ = '{{ cookiecutter.version }}'


from extras.plugins import PluginConfig


class {{ cookiecutter.__model_name }}Config(PluginConfig):
    name = '{{ cookiecutter.project_slug }}'
    verbose_name = '{{ cookiecutter.project_name }}'
    description = '{{ cookiecutter.project_short_description }}'
    version = 'version'
    base_url = '{{ cookiecutter.project_slug }}'


config = {{ cookiecutter.__model_name }}Config
