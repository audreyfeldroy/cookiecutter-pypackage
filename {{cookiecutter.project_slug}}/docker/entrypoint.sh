#!/bin/bash --login
set -e

conda activate $HOME/app/env
exec "$@"
