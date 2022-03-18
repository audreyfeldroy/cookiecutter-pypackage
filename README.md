# Cookiecutter PyPackage

[Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for a Python package,
adapted from [audreyfeldroy](https://github.com/audreyfeldroy).

* GitHub repo: https://github.com/audreyfeldroy/cookiecutter-pypackage/
* Documentation: https://cookiecutter-pypackage.readthedocs.io/
* Free software: BSD license

## Quickstart

Install the latest Cookiecutter if you haven't installed it yet (this requires
Cookiecutter 1.4.0 or higher):

```
pip install -U cookiecutter
```

Generate a Python package project:

```
cookiecutter https://github.com/ihumphrey/cookiecutter-pypackage.git
```

Create a new repo on GitHub, `git init` the created python package project, and push it up to the new repo:

```
cd [package_name]
git init .
git remote add origin git@github.com:[username]/[package_name].git
git branch -M main
git push -u origin main
```

Create a venv or conda environment.

Install versioneer:

```
pip install -U versioneer
versioneer install
git add -u
git commit -m "install versioneer"
git push
```

Install the package for local development:

```
pip install -e .[docs, tests]
```

Setup Codecov:
* On codecov.io, copy API token
* On repo's GitHub page, go to `Settings -> Secrets -> Actions -> New Repository Secret`
* Enter `CODECOV_TOKEN` as the name
* Paste the token in

Setup Readthedocs:
* https://readthedocs.org/accounts/login/, login with GitHub credentials, import the repo

Setup CodeClimate Quality
* https://codeclimate.com/login (Use GitHub credentials)

Setup PyPI for releases:
* Login to pypi account
* When you want to release:
* [Register](https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives) your project with PyPI.
* Update ``requirements.txt`` file that specifies the packages you will need for
  your project and their versions. For more info see the 
  [pip docs for requirements files](https://pip.pypa.io/en/stable/user_guide/#requirements-files)
* Release your package by pushing a new tag to main (master); this will generate a GitHub release and PyPI release.
* DOI

For more details, see the [cookiecutter-pypackage tutorial](https://cookiecutter-pypackage.readthedocs.io/en/latest/tutorial.html)




