{% set is_open_source = cookiecutter.open_source_license != 'Proprietary' -%}
{% for _ in cookiecutter.project_name %}={% endfor %}
{{ cookiecutter.project_name }}
{% for _ in cookiecutter.project_name %}={% endfor %}

{% if is_open_source %}
.. image:: https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg
        :target: https://pypi.python.org/pypi/{{ cookiecutter.project_slug }}

.. image:: https://readthedocs.org/projects/{{ cookiecutter.project_slug | replace("_", "-") }}/badge/?version=latest
        :target: https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
{%- endif %}

{% if cookiecutter.add_pyup_badge == 'y' %}
.. image:: https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/shield.svg
     :target: https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/
     :alt: Updates
{% endif %}


{{ cookiecutter.project_short_description }}

{% if is_open_source %}
* Free software: {{ cookiecutter.open_source_license }}
{% else %}
* Copyright (c) {% now 'local', '%Y' %}, {{ cookiecutter.full_name }} 
{% endif %}
* Documentation: https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io.

Features
--------

* TODO


Quickstart
----------

1. `pip install {{ cookiecutter.project_slug }}`
2. ...
3. Profit!


Testing
-------

Test with Nox:

    # run everything
    nox
    
    # run tests only
    nox -s tests

    # run everything but tests and linting
    nox -k "not tests and not lint"



Credits
-------

This package was created with Cookiecutter_ and the `inhumantsar/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`inhumantsar/cookiecutter-pypackage`: https://github.com/inhumantsar/cookiecutter-pypackage
