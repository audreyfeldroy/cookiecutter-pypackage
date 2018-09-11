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

It is also possible to test your code using `tox` locally, or
```
$ docker build -t foo . && docker run -it foo
```

## Versioning

This package uses [bumpversion](https://github.com/c4urself/bump2version).

The workflow to create a new version is as follows:

1. Use
```
pipenv run bumpversion [major|minor|patch]
```
or, depending on your setup, simply
```
bumpversion [major|minor|patch]
```
to increment to the next major, minor or patch version number, at pre-release `rc.1`.
You can do this at any time, either after a full release, or in the middle of a pre-release.

2. To then create a second (or third) `rc` pre-release
```
bumpversion rc
```

3. If you are satisfied with an `rc` pre-release version, to build the final release
```
bumpversion release
```

`bumpversion` creates both a commit and a tag, pushing the tag to github triggers a release
build, and circleci will push a package to [packagecloud](https://packagecloud.io/syapse/General).
