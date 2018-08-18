#!/bin/bash -e

older_python_versions=3.6.5
python_version=3.7.0

# Get latest version from here: https://www.python.org/downloads/
for ver in $older_python_versions $python_version
do
  pyenv install -s ${ver:?}
done
pyenv virtualenv ${python_version:?} "$(cut -d' ' -f1 < .python-version)" || true
pip install --upgrade pip
pip install -r requirements_dev.txt
pip install -e .
