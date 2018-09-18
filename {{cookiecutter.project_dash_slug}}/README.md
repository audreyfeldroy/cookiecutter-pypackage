# {{cookiecutter.project_name}}

{{cookiecutter.project_short_description}}


## Quickstart

Please enable circleci on the new repo.

Please run:
```
pipenv install -e .
```
To create `Pipfile.lock` which should be committed and pushed to the repo (and
updated from time to time, especially after changes to the requirements in `setup.cfg`)


## Testing

Please add your tests
to the `tests` folder, with supporting data in the `test-data` folder.

Locally use the following command to run the tests:
```
pipenv run python -m unittest discover -s tests -t . -p '*.py'
```

To test your code on all supported versions of python, please push to github,
and look at [CircleCI](https://circleci.com/gh/syapse/{{ cookiecutter.project_dash_slug }}).

To build a release, tag a commit (see below), and the built package will be
uploaded to packagecloud.

## Versioning

This package uses [bumpversion](https://github.com/c4urself/bump2version).

To go to the next major/minor/patch/rc version, the command:
```
pipenv run bumpversion [major|minor|patch|rc]
```
works. If the current version is a pre-release rc version, or you wish to create the first
pre-release rc version for the next release, then you have to manually specify the version number
(and a further ignored argument).
e.g. If current version is 1.3.2, you may choose to do
```
pipenv run bumpversion ignored-arg --new-version 1.4.0-rc1
```
then when the pre-release process is complete for 1.4.0 you can call
```
pipenv run bumpversion ignored-arg --new-version 1.4.0
```
to complete the release.

`bumpversion` both creates a commit and a tag, pushing the tag to github triggers a release
build, and circleci will push a package to [packagecloud](https://packagecloud.io/syapse/General).
