# Development

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

## Making a release

Related backlog tasks:

* Do release of cookiecutter-pypackage projects in CircleCI (after other tests pass)

First, make sure version has been bumped:

```sh
git checkout main
git pull
git stash
last_released_version=v"$(python -c 'import op_env; print(op_env.__version__)')"
git log ${last_released_version:?}..
bumpversion # give it major, minor or patch
git push
git push --tags
make release
git stash pop
open https://pypi.org/project/op_env
```
