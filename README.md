# Syapse Python Package Cookiecutter

## Prerequisites

* [Python](https://www.python.org/) 2.7, 3.6, and/or 3.7

## Quickstart

```
# Install cookiecutter
$ pip install cookiecutter

# Generate a new project
$ cookiecutter git@github.com:syapse/cookiecutter-pypackage.git

# Follow the prompts to configure your project. See Cookiecutter Options below.

You are strongly advised to follow the naming convention of starting your project name
with 'Syapse', and hence your package name with 'syapse_'. This is to avoid name
collisions with packages at [PyPI](https://pypi.org)


## Cookiecutter Options

The following options can be specified when creating a new service.

| Prompt                      | Description                                                                              |
| --------------------------- | -----------------------------------------------------------------------------------------|
| `project_name`              | The human-readable name of the new project (Should start with 'Syapse').                 |
| `project_slug`              | The Python-compatible identifier of the generated module. Must start 'syapse_'.          |
| `project_dash_slug`         | The top-level directory name, conventionally avoiding _.                                 |
| `project_short_description` | A few words about the project.                                                           |
| `python_2_7`                | Include python 2.7 support.                                                              |
| `version`                   | Semantic Version number.                                                                 |
| `command_line_interface`    | Whether to provide a command line tool.                                                  |
| `enable_packagecloud`       | Whether you wish to use further libraries from packagecloud.                             |
| `packagecloud_read_token`   | Accept default value to be guided through creating one.                                  |
