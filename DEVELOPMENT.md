# Development

## Adding or removing a Python version

To add or remove a supported Python version:

If adding, first add the new Python version in docker-circleci to
ensure fast builds afterwards.

Then, update cookiecutter-cookiecutter with the following:

1. Grep for and change areas surrounding the existing used version
2. Do the same for an existing version's tox environment

Update cookiecutter-cookiecutter from itself and then update
cookiecutter-pypackage from cookiecutter-cookiecutter.

Then, in cookiecutter-pypackage:

1. Grep for and change areas surrounding the existing used version
2. Do the same for an existing version's tox environment

You may encounter the following problems:

* Subtle changes in behavior in argparse affecting CLI tests (add an
  if statement).
* Libraries that don't yet have binary versions published (add a
  binary dependency in fix.sh)

## fix.sh

If you want to use rbenv/pyenv/etc to manage versions of tools,
there's a `fix.sh` script which may be what you'd like to install
dependencies.

## Overcommit

This project uses [overcommit](https://github.com/sds/overcommit) for
quality checks.  `bundle exec overcommit --install` will install it.

## direnv

This project uses direnv to manage environment variables used during
development.  See the `.envrc` file for detail.

## Tests

To get full realtime output from tests to debug e.g. slowness issues:

```sh
pytest tests/test_bake_project.py --capture=no -k test_bake_and_run_build
```

You can debug overall test timings with:

```sh
time pytest tests/test_bake_project.py --durations=0
```

It's also useful to replace 'make test' with something that will give
you real-time stdout/stderr in `test_bake_project.py`.

You can then wrap `time` commands around different things that shell
out, or do [this type of
technique](https://stackoverflow.com/a/1557584/2625807) for things
which aren't a simple shell-out.
