#!/bin/bash

set -e

require() {
    type $1 >/dev/null 2>/dev/null
}

cleanup() {
    rm -rf python_boilerplate
}
trap cleanup EXIT


require cookiecutter

echo "Running test script..."
cookiecutter . --no-input
(
    cd ./python_boilerplate
    pip install -r requirements_dev.txt
    python setup.py test
    python travis_pypi_setup.py --repo audreyr/cookiecutter-pypackage --password invalidpass
    python -c '''import yaml
assert "secure" in yaml.load(open(".travis.yml"))["deploy"]["password"],\
    ".travis.yml missing password config"'''
)

echo Done
