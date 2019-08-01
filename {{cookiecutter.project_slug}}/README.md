{% set is_open_source = cookiecutter.open_source_license != 'Not open source' -%} 
{% for _ in cookiecutter.project_name %}={% endfor%} {{ cookiecutter.project_name }} {% for _ in cookiecutter.project_name %}={% endfor %}

{% if is_open_source %} 
[![PiPy Badge](https://img.shields.io/pypi/v/{{cookiecutter.project_slug }}.svg)](https://pypi.python.org/pypi/{{ cookiecutter.project_slug }})

[![Travis Badge](https://img.shields.io/travis/{{cookiecutter.github_account }}{{cookiecutter.project_slug }}.svg)](https://travis-ci.org/{{cookiecutter.github_account }}{{cookiecutter.project_slug }})

[![Documentation Status](https://readthedocs.org/projects/{{ cookiecutter.project_slug | replace("_", "-") }}/badge/?version=latest)](https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io/en/latest/?badge=latest)
{%- endif %}

{% if cookiecutter.add_pyup_badge == 'y' %}
[![Shield](https://pyup.io/repos/github/{{ cookiecutter.github_account }}/{{cookiecutter.project_slug }}/shield.svg)](https://pyup.io/repos/github/{{ cookiecutter.github_account }}/{{cookiecutter.project_slug }}/)
{% endif %}

{{ cookiecutter.project_short_description }}

{% if is_open_source %} 
* Free software: {{cookiecutter.open_source_license }} 
* Documentation: [readthedocs.io](https://{{cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io/)
{% endif %}

Features
========

-   TODO

Credits
=======

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[steadysense/cookiecutter-pypackage](https://github.com/steadysense/cookiecutter-pypackage)
project template.
