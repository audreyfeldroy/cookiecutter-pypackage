#!/bin/bash

set -eou pipefail

echo "create git repo for pre-commit"
git init .

# the following hooks take a while to execute
# export COOKIECUTTER_SKIP_POST_GEN_HOOK to 1 to skip the following hooks
COOKIECUTTER_SKIP_POST_GEN_HOOK="${COOKIECUTTER_SKIP_POST_GEN_HOOK:-0}"

if [ "$COOKIECUTTER_SKIP_POST_GEN_HOOK" != "1" ]
then
    echo "Generating lock file"
    pip-compile -o requirements.txt pyproject.toml --quiet

    echo "Generating dev lock file"
    pip-compile --extra dev -o requirements_dev.txt pyproject.toml --quiet
else
    echo "Skipping long post gen hooks"
fi

echo "Finished"
