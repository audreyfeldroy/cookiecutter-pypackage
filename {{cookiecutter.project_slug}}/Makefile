VERSION := {{ cookiecutter.version }}
RELEASE := master

# Include custom config if it is available
-include Makefile.config

# Application
APP_ROOT := $(CURDIR)
APP_NAME := $(shell basename $(APP_ROOT))

# guess OS (Linux, Darwin, ...)
OS_NAME := $(shell uname -s 2>/dev/null || echo "unknown")
CPU_ARCH := $(shell uname -m 2>/dev/null || uname -p 2>/dev/null || echo "unknown")

# Python
SETUPTOOLS_VERSION := 36.5.0
CONDA_VERSION := 4.4
BUILDOUT_VERSION := 2.10.0

# Anaconda
ANACONDA_HOME ?= $(HOME)/anaconda
CONDA_ENV ?= $(APP_NAME)
CONDA_ENVS_DIR ?= $(HOME)/.conda/envs
CONDA_ENV_PATH := $(CONDA_ENVS_DIR)/$(CONDA_ENV)
CONDA_PINNED := $(APP_ROOT)/requirements/conda_pinned

# Configuration used by update-config
HOSTNAME ?= localhost
HTTP_PORT ?= 8094
OUTPUT_PORT ?= 8090

# choose anaconda installer depending on your OS
ANACONDA_URL = https://repo.continuum.io/miniconda
ifeq "$(OS_NAME)" "Linux"
FN := Miniconda2-latest-Linux-x86_64.sh
else ifeq "$(OS_NAME)" "Darwin"
FN := Miniconda2-latest-MacOSX-x86_64.sh
else
FN := unknown
endif

# Buildout files and folders
DOWNLOAD_CACHE := $(APP_ROOT)/downloads
BUILDOUT_FILES := parts eggs develop-eggs bin .installed.cfg .mr.developer.cfg *.egg-info bootstrap-buildout.py *.bak.* $(DOWNLOAD_CACHE)

# Docker
DOCKER_IMAGE := birdhouse/$(APP_NAME)
DOCKER_CONTAINER := $(APP_NAME)

# end of configuration


.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint: ## check style with flake8
	flake8 {{ cookiecutter.project_slug }} tests

#test: ## run tests quickly with the default Python
#{%- if cookiecutter.use_pytest == 'y' %}
#	py.test
#{%- else %}
#	python setup.py test
#{%- endif %}

#test-all: ## run tests on every Python version with tox
#	tox

coverage: ## check code coverage quickly with the default Python
{%- if cookiecutter.use_pytest == 'y' %}
	coverage run --source {{ cookiecutter.project_slug }} -m pytest
{%- else %}
	coverage run --source {{ cookiecutter.project_slug }} setup.py test
{%- endif %}
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/{{ cookiecutter.project_slug }}.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ {{ cookiecutter.project_slug }}
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: clean ## package and upload a release
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

version: ## Print the version number
	@echo "Version: $(VERSION)"

info: ## Print information about the bird
	@echo "Informations about your Bird:"
	@echo "  OS_NAME             $(OS_NAME)"
	@echo "  CPU_ARCH            $(CPU_ARCH)"
	@echo "  Anaconda Home       $(ANACONDA_HOME)"
	@echo "  Conda Environment   $(CONDA_ENV). Use \`source activate $(CONDA_ENV)' to activate it."
	@echo "  Conda Prefix        $(CONDA_ENV_PATH)"
	@echo "  APP_NAME            $(APP_NAME)"
	@echo "  APP_ROOT            $(APP_ROOT)"
	@echo "  DOWNLOAD_CACHE      $(DOWNLOAD_CACHE)"
	@echo "  DOCKER_IMAGE        $(DOCKER_IMAGE)"

## EMU ##

## Helper targets ... ensure that Makefile etc are in place

backup: ## Backup custom configuration.
	@echo "Backup custom config ..."
	@-test -f custom.cfg && cp -v --update --backup=numbered --suffix=.bak custom.cfg custom.cfg.bak

.gitignore: ## Checkout .gitignore file.
	@echo "Setup default .gitignore ..."
	@curl "https://raw.githubusercontent.com/bird-house/birdhousebuilder.bootstrap/$(RELEASE)/dot_gitignore" --silent --insecure --output .gitignore

bootstrap.sh: ## Checkout bootstrap.sh
	@echo "Update bootstrap.sh ..."
	@curl "https://raw.githubusercontent.com/bird-house/birdhousebuilder.bootstrap/$(RELEASE)/bootstrap.sh" --silent --insecure --output bootstrap.sh "https://raw.githubusercontent.com/bird-house/birdhousebuilder.bootstrap/$(RELEASE)/bootstrap.sh"
	@chmod 755 bootstrap.sh

custom.cfg: ## Use custom.cfg for buildout
	@echo "Using custom.cfg for buildout ..."
	@test -f custom.cfg || cp -v custom.cfg.example custom.cfg

downloads: ## Create download cache directory if it does not exist.
	@echo "Using DOWNLOAD_CACHE $(DOWNLOAD_CACHE)"
	@test -d $(DOWNLOAD_CACHE) || mkdir -v -p $(DOWNLOAD_CACHE)

init: custom.cfg downloads

bootstrap-buildout.py: ## Checkout the bootstrap-buildout.py file
	@echo "Update buildout bootstrap-buildout.py ..."
	@test -f boostrap-buildout.py || curl https://bootstrap.pypa.io/bootstrap-buildout.py --insecure --silent --output bootstrap-buildout.py

## Anaconda targets

anaconda: ## Install Anaconda
	@echo "Installing Anaconda ..."
	@test -d $(ANACONDA_HOME) || curl $(ANACONDA_URL)/$(FN) --silent --insecure --output "$(DOWNLOAD_CACHE)/$(FN)"
	@test -d $(ANACONDA_HOME) || bash "$(DOWNLOAD_CACHE)/$(FN)" -b -p $(ANACONDA_HOME)
	@echo "Add '$(ANACONDA_HOME)/bin' to your PATH variable in '.bashrc'."

conda_config: anaconda ## Configure conda
	@echo "Update ~/.condarc"
	@-"$(ANACONDA_HOME)/bin/conda" install -y conda=$(CONDA_VERSION) requests
	@"$(ANACONDA_HOME)/bin/conda" config --add envs_dirs $(CONDA_ENVS_DIR)
	@"$(ANACONDA_HOME)/bin/conda" config --set ssl_verify true
	@"$(ANACONDA_HOME)/bin/conda" config --set use_pip true
	@"$(ANACONDA_HOME)/bin/conda" config --set channel_priority true
	@"$(ANACONDA_HOME)/bin/conda" config --set auto_update_conda false
	@"$(ANACONDA_HOME)/bin/conda" config --add channels defaults
	@"$(ANACONDA_HOME)/bin/conda" config --append channels birdhouse
	@"$(ANACONDA_HOME)/bin/conda" config --append channels conda-forge

conda_env: anaconda conda_config  ## Update conda environment
	@echo "Update conda environment $(CONDA_ENV) ..."
	@test -d $(CONDA_ENV_PATH) || "$(ANACONDA_HOME)/bin/conda" env create -n $(CONDA_ENV) -f environment.yml
	"$(ANACONDA_HOME)/bin/conda" install -y -n $(CONDA_ENV) setuptools=$(SETUPTOOLS_VERSION)

conda_pinned: conda_env
	@echo "Update pinned conda packages ..."
	@-test -d $(CONDA_ENV_PATH) && test -f $(CONDA_PINNED) && cp -f "$(CONDA_PINNED)" "$(CONDA_ENV_PATH)/conda-meta/pinned"

export: ## Export conda environment
	@echo "Exporting conda enviroment ..."
	@test -d $(CONDA_ENV_PATH) && "$(ANACONDA_HOME)/bin/conda" env export -n $(CONDA_ENV) -f environment.yml

## Build targets

bootstrap: init conda_env conda_pinned bootstrap-buildout.py ## Bootstrap buildout
	@echo "Bootstrap buildout ..."
	@test -f bin/buildout || bash -c "source $(ANACONDA_HOME)/bin/activate $(CONDA_ENV);python bootstrap-buildout.py -c custom.cfg --allow-site-packages --setuptools-version=$(SETUPTOOLS_VERSION) --buildout-version=$(BUILDOUT_VERSION)"

sysinstall: ## Install system packages for bootstrap
	@echo "\nInstalling system packages for bootstrap ..."
	@bash bootstrap.sh -i
	@echo "\nInstalling system packages for your application ..."
	@-test -f requirements.sh && bash requirements.sh

install: bootstrap ## Install {{cookiecutter.project_name}}
	@echo "Installing application with buildout ..."
	@-bash -c "source $(ANACONDA_HOME)/bin/activate $(CONDA_ENV);bin/buildout buildout:anaconda-home=$(ANACONDA_HOME) -c custom.cfg"
	@echo "\nStart service with \`make start'"

update: ## Update application configuration with buildout
	@echo "Update application config with buildout (offline mode) ..."
	@-bash -c "source $(ANACONDA_HOME)/bin/activate $(CONDA_ENV);bin/buildout buildout:anaconda-home=$(ANACONDA_HOME) -o -c custom.cfg"

update-config: ## Update application config with buildout (offline mode) and environment variables
	@echo "Update application config with buildout (offline mode) and environment variables..."
	@-bash -c "source $(ANACONDA_HOME)/bin/activate $(CONDA_ENV);bin/buildout buildout:anaconda-home=$(ANACONDA_HOME) settings:hostname=$(HOSTNAME) settings:output-port=$(OUTPUT_PORT) settings:http-port=$(HTTP_PORT) -o -c custom.cfg"

clean: srcclean envclean ## Clean buildout files
	@echo "Cleaning buildout files ..."
	@-for i in $(BUILDOUT_FILES); do \
            test -e $$i && rm -v -rf $$i; \
        done

envclean: stop ## Remove conda environment
	@echo "Removing conda env $(CONDA_ENV)"
	@-test -d $(CONDA_ENV_PATH) && "$(ANACONDA_HOME)/bin/conda" remove -n $(CONDA_ENV) --yes --all

srcclean: ## Remove *.pyc files
	@echo "Removing *.pyc files ..."
	@-find $(APP_ROOT) -type f -name "*.pyc" -print | xargs rm

distclean: backup clean ## Clean distribution
	@echo "Cleaning distribution ..."
	@git diff --quiet HEAD || echo "There are uncommited changes! Not doing 'git clean' ..."
	@-git clean -dfx -e *.bak -e custom.cfg -e Makefile.config

passwd: custom.cfg  ## Generate a Phoenix password
	@echo "Generate Phoenix password ..."
	@echo "Enter a password with at least 8 characters."
	@bash -c "source $(ANACONDA_HOME)/bin/activate $(CONDA_ENV); python -c 'from IPython.lib import passwd; pw = passwd(algorithm=\"sha256\"); lines = [\"phoenix-password = \" + pw + \"\\n\" if line.startswith(\"phoenix-password\") else line for line in open(\"custom.cfg\", \"r\")]; file = open(\"custom.cfg\", \"w\"); file.writelines(lines); file.close()'"
	@echo ""
	@echo "Run \`make install restart' to activate this password."

test: ## Run tests (skip slow and online tests)
	@echo "Running tests (skip slow and online tests) ..."
	bash -c "source $(ANACONDA_HOME)/bin/activate $(CONDA_ENV); bin/py.test -v -m 'not slow and not online'"

testall: ## Run all tests
	@echo "Running all tests (including slow and online tests) ..."
	bash -c "source $(ANACONDA_HOME)/bin/activate $(CONDA_ENV); bin/py.test -v"

pep8: ## PEP8 code style checks
	@echo "Running pep8 code style checks ..."
	$(CONDA_ENV_PATH)/bin/flake8

#docs:
#	@echo "Generating docs with Sphinx ..."
#	$(MAKE) -C $@ clean html
#	@echo "open your browser: firefox docs/build/html/index.html"

linkcheck: ## Run link checker
	@echo "Run link checker on docs..."
	$(MAKE) -C docs linkcheck

doc8: ## Run doc8 doc style checks
	@echo "Running doc8 doc style checks ..."
	$(CONDA_ENV_PATH)/bin/doc8 docs/

selfupdate: bootstrap.sh .gitignore ## TODO
	@curl "https://raw.githubusercontent.com/bird-house/birdhousebuilder.bootstrap/$(RELEASE)/Makefile" --silent --insecure --output Makefile

## Supervisor targets

start: ## Launch server
	@echo "Starting supervisor service ..."
	bin/supervisord start

stop: ## Stop server
	@echo "Stopping supervisor service ..."
	-bin/supervisord stop

restart: ## Restart server
	@echo "Restarting supervisor service ..."
	bin/supervisord restart

status: ## Print server status
	@echo "Supervisor status ..."
	bin/supervisorctl status


## Docker targets

Dockerfile: bootstrap ## Update Dockerfile
	@echo "Update Dockerfile ..."
	bin/buildout -c custom.cfg install docker

dockerrmi: ## Remove docker image
	@echo "Removing previous docker image ..."
	docker rmi $(DOCKER_IMAGE)

dockerbuild: Dockerfile ## Build docker image
	@echo "Building docker image ..."
	docker build --rm -t $(DOCKER_IMAGE) .

dockerrun: dockerbuild ## Run docker image
	@echo "Run docker image ..."
	docker run -i -t -p 9001:9001 --name=$(DOCKER_CONTAINER) $(DOCKER_IMAGE) /bin/bash
