{% set is_open_source = cookiecutter.open_source_license != 'Not open source' -%}
{% for _ in cookiecutter.project_name %}={% endfor %}
{{ cookiecutter.project_name }}
{% for _ in cookiecutter.project_name %}={% endfor %}

{% if is_open_source %}
.. image:: https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg
        :target: https://pypi.python.org/pypi/{{ cookiecutter.project_slug }}

{% if cookiecutter.use_travis_ci == 'y' -%}
.. image:: https://img.shields.io/travis/{{ cookiecutter.repo_username }}/{{ cookiecutter.project_slug }}.svg
        :target: https://travis-ci.org/{{ cookiecutter.repo_username }}/{{ cookiecutter.project_slug }}
{%- endif %}

{% if cookiecutter.use_read_the_docs == 'y' -%}
.. image:: https://readthedocs.org/projects/{{ cookiecutter.project_slug | replace("_", "-") }}/badge/?version=latest
        :target: https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
{%- endif %}
{%- endif %}

{{ cookiecutter.project_short_description }}

{% if is_open_source -%}
* Free software: {{ cookiecutter.open_source_license }}
{%- else -%}
* Propertiary software of {{ cookiecutter.copyright }}, please obtain a license before use.
{%- endif %}
{% if cookiecutter.use_read_the_docs == 'y' -%}
* Documentation: https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io.
{%- endif %}

Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_ and the `wooyek/cookiecutter-pylib`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`wooyek/cookiecutter-pylib`: https://github.com/wooyek/cookiecutter-pylib

