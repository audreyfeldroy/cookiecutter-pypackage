{% set is_open_source = cookiecutter.open_source_license != 'Not open source' -%}
{% for _ in cookiecutter.project_name %}={% endfor %}
{{ cookiecutter.project_name }}
{% for _ in cookiecutter.project_name %}={% endfor %}

{% if is_open_source %}
.. image:: https://badge.fury.io/py/{{ cookiecutter.project_slug }}.svg
    :target: https://badge.fury.io/py/{{ cookiecutter.project_slug }}
.. image:: https://readthedocs.org/projects/{{ cookiecutter.project_slug | replace("_", "-") }}/badge/?version=latest
    :target: https://{{ cookiecutter.project_slug }}.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://circleci.com/gh/{{ cookiecutter.git_username }}/{{ cookiecutter.project_slug | replace("_", "-") }}.svg?style=shield
    :target: https://circleci.com/gh/{{ cookiecutter.git_username }}/{{ cookiecutter.project_slug | replace("_", "-") }}
{%- endif %}

{% if cookiecutter.add_pyup_badge == 'y' %}
.. image:: https://pyup.io/repos/github/{{ cookiecutter.git_username }}/{{ cookiecutter.project_slug }}/shield.svg
     :target: https://pyup.io/repos/github/{{ cookiecutter.git_username }}/{{ cookiecutter.project_slug }}/
     :alt: Updates
{% endif %}
.. image:: https://mybinder.org/badge_logo.svg
    :target: https://mybinder.org/v2/gh/pyfar/gallery/main?filepath=docs/gallery


{{ cookiecutter.project_short_description }}

{% if is_open_source %}
* Free software: {{ cookiecutter.open_source_license }}
{% endif %}

Getting Started
===============

Check out `pyfar.org`_ for a tour through the pyfar
universe, including complete documentation of this package and
the other packages.

Installation
============

Use pip to install {{ cookiecutter.project_slug }}

.. code-block:: console

    $ pip install {{ cookiecutter.project_slug }}

(Requires Python {{ cookiecutter.minimum_python_version }} or higher)

Contributing
============

Refer to the `contribution guidelines`_ for more information.


.. _contribution guidelines: https://github.com/{{ cookiecutter.git_username }}/{{ cookiecutter.project_slug }}/blob/develop/CONTRIBUTING.rst
.. _pyfar.org: https://pyfar.org
.. _read the docs: https://{{ cookiecutter.project_slug }}.readthedocs.io/en/latest
