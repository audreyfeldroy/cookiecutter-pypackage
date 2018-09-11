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

# To test locally (2.7 and 3.6 only) you can use tox, if setup correctly (black magic):
$ tox

# To avoid black magic, use Docker for local testing
$ docker build -t foo . && docker run -it foo
```

## Cookiecutter Options

The following options can be specified when creating a new service.

| Prompt                        | Description                                                                              |
| ----------------------------- | -----------------------------------------------------------------------------------------|
| `project_name`                | The human-readable name of the new project  .                                            |
| `project_slug`                | The name of the Python module to generate. Must be a Python-compatible identifier.       |
| `project_dash_slug`           | The top-level directory name, conventionally avoiding _.                                 |
| `project_short_description`   | A few words about the project.                                                           |
| `version`                     | Semantic Version number.                                                                 |
| `command_line_interface`      | Whether to provide a command line tool.                                                  |
| `optional_packagecloud_token` | The token for accessing package cloud. (Do not include in this __public__ repo.)         |
