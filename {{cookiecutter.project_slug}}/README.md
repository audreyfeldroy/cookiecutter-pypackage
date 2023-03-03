![tests workflow](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug | replace("_", "-") }}/actions/workflows/test.yml/badge.svg)
![lint workflow](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug | replace("_", "-") }}/actions/workflows/pylint.yml/badge.svg)
{% if cookiecutter.use_pre_commit == 'y' -%}
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
{%- endif %}

{% set is_open_source = cookiecutter.open_source_license != 'Not open source' -%}
# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

{% if is_open_source %}
* Free software: {{ cookiecutter.open_source_license }}
* Documentation: https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io.
{% endif %}


# Contributing

To work on this project, install the development requirements by running:
```
make install
```

# Tests

```
make tests
```

# Credits

This package was created with **[Cookiecutter](https://github.com/audreyr/cookiecutter)** and the **[`audreyr/cookiecutter-pypackage`](https://github.com/audreyr/cookiecutter-pypackage)** project template.
