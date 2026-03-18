# Installation

## Stable release

To install {{ cookiecutter.project_name }}, run this command in your terminal:

```sh
uv add {{ cookiecutter.package_name }}
```

Or if you prefer to use `pip`:

```sh
pip install {{ cookiecutter.package_name }}
```

## From source

The source files for {{ cookiecutter.project_name }} can be downloaded from the [Github repo](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}).

You can either clone the public repository:

```sh
git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}
```

Or download the [tarball](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}/tarball/main):

```sh
curl -OJL https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}/tarball/main
```

Once you have a copy of the source, you can install it with:

```sh
cd {{ cookiecutter.package_name }}
uv sync
```
