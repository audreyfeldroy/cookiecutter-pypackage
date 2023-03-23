# Mansueto Cookiecutter PyPackage

An opinionated Cookiecutter to create a new Python package.

- CI/CD: [bump2version](https://github.com/c4urself/bump2version), [Github Actions](https://github.com/features/actions)
- Code Style: [flake8](https://github.com/PyCQA/flake8) and [isort](https://github.com/timothycrosley/isort)
- Documentation: [Sphinx](https://github.com/sphinx-doc/sphinx)
- Tests: [pytest](https://github.com/pytest-dev/pytest), [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) and [pytest-mock](https://github.com/pytest-dev/pytest-mock/)

``` text
├── CHANGELOG.rst
├── docs
│   ├── changelog.rst
│   ├── conf.py
│   ├── index.rst
│   ├── make.bat
│   ├── Makefile
│   ├── readme.rst
│   └── usage.rst
├── .github
│   ├── dependabot.yml
│   └── workflows
│       └── python-app.yml
├── .gitignore
├── LICENSE
├── MANIFEST.in
├── .pre-commit-config.yaml
├── python_boilerplate
│   ├── __init__.py
│   └── python_boilerplate.py
├── README.rst
├── requirements_dev.txt
├── setup.cfg
├── setup.py
├── tests
│   ├── __init__.py
│   └── test_python_boilerplate.py
```

## How to Use

```bash
pip install -U cookiecutter
cookiecutter https://github.com/mansueto-institute/cookiecutter-pypackage
```
