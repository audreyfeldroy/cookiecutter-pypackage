{% set is_open_source = cookiecutter.copyright_license != 'Proprietary' -%}
{% for _ in cookiecutter.repository_name %}={% endfor %}
{{ cookiecutter.repository_name }}
{% for _ in cookiecutter.repository_name %}={% endfor %}

{% if is_open_source %}
.. image:: https://img.shields.io/pypi/v/{{ cookiecutter.module_name }}.svg
        :target: https://pypi.python.org/pypi/{{ cookiecutter.module_name }}

.. image:: https://img.shields.io/travis/{{ cookiecutter.remote_username }}/{{ cookiecutter.module_name }}.svg
        :target: https://travis-ci.org/{{ cookiecutter.remote_username }}/{{ cookiecutter.module_name }}

.. image:: https://readthedocs.org/projects/{{ cookiecutter.module_name | replace("_", "-") }}/badge/?version=latest
        :target: https://{{ cookiecutter.module_name | replace("_", "-") }}.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
{%- endif %}

.. image:: https://pyup.io/repos/github/{{ cookiecutter.remote_username }}/{{ cookiecutter.module_name }}/shield.svg
     :target: https://pyup.io/repos/github/{{ cookiecutter.remote_username }}/{{ cookiecutter.module_name }}/
     :alt: Updates


{{ cookiecutter.repository_summary }}

{% if is_open_source %}
* Free software: {{ cookiecutter.copyright_license }}
* Documentation: https://{{ cookiecutter.module_name | replace("_", "-") }}.readthedocs.io.
{% endif %}

Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_ and the custom `moodule/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

