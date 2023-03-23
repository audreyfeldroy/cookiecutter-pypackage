# Mansueto Cookiecutter PyPackage

An opinionated Cookiecutter to create a new Python package.

- CI/CD: [bump2version](https://github.com/c4urself/bump2version), [Github Actions](https://github.com/features/actions)
- Code Style: [black](https://black.readthedocs.io/en/stable/), [flake8](https://github.com/PyCQA/flake8), [isort](https://github.com/timothycrosley/isort)
- Documentation: [Sphinx](https://github.com/sphinx-doc/sphinx)
- Tests: [mypy](https://mypy.readthedocs.io/en/stable/index.html), [pytest](https://github.com/pytest-dev/pytest), [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/), [pytest-mock](https://github.com/pytest-dev/pytest-mock/)

## Directory Structure

``` text
├── AUTHORS.rst
├── CONTRIBUTING.rst
├── HISTORY.rst
├── LICENSE
├── MANIFEST.in
├── Makefile
├── README.md
├── docs
│   ├── Makefile
│   ├── authors.rst
│   ├── conf.py
│   ├── contributing.rst
│   ├── history.rst
│   ├── index.rst
│   ├── installation.rst
│   ├── make.bat
│   ├── readme.rst
│   └── usage.rst
├── pyproject.toml
├── requirements.txt
├── setup.cfg
├── src
│   └── python_boilerplate
│       ├── __init__.py
│       ├── cli.py
│       └── python_boilerplate.py
└── tests
    ├── __init__.py
    └── test_python_boilerplate.py
```

## How to Use

```bash
pip install -U cookiecutter
cookiecutter https://github.com/mansueto-institute/cookiecutter-pypackage
```
