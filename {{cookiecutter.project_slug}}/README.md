{% set is_open_source = cookiecutter.open_source_license != 'Not open source' -%}
# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

{% if is_open_source %}
* Free software: {{ cookiecutter.open_source_license }}
* Documentation: https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io.
{% endif %}

# Features

* TODO

# Installation


## Stable release

To install {{ cookiecutter.project_name }}, run this command in your terminal:

```bash
pip install {{ cookiecutter.project_slug }}
```

This is the preferred method to install {{ cookiecutter.project_name }}, as it will always install the most recent stable release.

If you don't have [`pip`](https://pip.pypa.io) installed, this [`Python installation guide`](https://docs.python-guide.org/en/latest/starting/installation/) can guide you through the process.


## From sources

The sources for {{ cookiecutter.project_name }} can be downloaded from the [`Github repo`](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}).

You can either clone the public repository:


```bash
git clone git://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}
```

Or download the [`tarball`](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/tarball/master):

```bash
curl -OJL https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/tarball/master
```

Once you have a copy of the source, you can install it with:

```bash
python setup.py install
```

# Usage

* TODO


# Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [lrivallain/cookiecutter-pypackage](https://github.com/lrivallain/cookiecutter-pypackage) project template.
