# Cookiecutter PyPackage

[Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for a Python package,
adapted from [audreyfeldroy](https://github.com/audreyfeldroy).

* GitHub repo: https://github.com/audreyfeldroy/cookiecutter-pypackage/
* Documentation: https://cookiecutter-pypackage.readthedocs.io/
* Free software: BSD license

## Quickstart

### Install cookiecutter

Install the latest Cookiecutter if you haven't installed it yet (this requires
Cookiecutter 1.4.0 or higher):

```
pip install -U cookiecutter
```

### Generate a Python package project

We will use cookiecutter to create your Python project.

<details>
 <summary>Click to see more information about how the project is generated.</summary>
 This will set up the structure of the project, the setup file, licensing files,
the Sphinx document generation tool, and a new GitHub workflow (`.github/workflows`)
that will automatically build and test your code for PRs and commits to the main branch.
It also allow you to create releases and distribute them in GitHub Releases and PyPI
when you push a new tag to the GitHub repo.
 </details>

```
cookiecutter https://github.com/ihumphrey/cookiecutter-pypackage.git
```

### Setup Repos

Create a new repo on GitHub, `git init` the created python package project, and push it up to the new repo:

```
cd [package_name]
git init .
git remote add origin git@github.com:[username]/[package_name].git
git branch -M main
git push -u origin main
```

Create a venv or conda environment.

### Setup versioneer

Install versioneer:

```
pip install -U versioneer
versioneer install
git add -u
git commit -m "install versioneer"
git push
```

### Install package for development

Install the package via an editable pip installation for local development:

```
pip install -e .[docs, tests]
```

### Setup Codecov:
* On codecov.io, copy API token
* On repo's GitHub page, go to `Settings -> Secrets -> Actions -> New Repository Secret`
* Enter `CODECOV_TOKEN` as the name
* Paste the token in

### Setup Readthedocs:
* https://readthedocs.org/accounts/login/, login with GitHub credentials, import the repo

### Setup CodeClimate Quality
* https://codeclimate.com/login (Use GitHub credentials)

### Setup PyPI for releases:
If you want to release and distribute your package via pip, you will need to register your project with PyPI.

* Login to or create a [PyPI](https://pypi.org/) account
* [Register](https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives) your project on PyPI
* Update ``requirements.txt`` file that specifies the packages you will need for
  your project and their versions. For more info see the 
  [pip docs for requirements files](https://pip.pypa.io/en/stable/user_guide/#requirements-files)
* Release your package by pushing a new tag to main (master); this will generate a GitHub release and PyPI release
via your CI GitHub Action
* DOI

For more details, see the [cookiecutter-pypackage tutorial](https://cookiecutter-pypackage.readthedocs.io/en/latest/tutorial.html)




