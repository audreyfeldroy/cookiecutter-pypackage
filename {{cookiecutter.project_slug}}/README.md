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
