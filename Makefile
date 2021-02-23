.PHONY: all clean test help quality
.DEFAULT_GOAL := default

BAKE_OPTIONS=--no-input

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


all: test quality

clean: ## remove all built artifacts

default: test ## run default typechecking and tests

test: ## run tests quickly
	pytest

quality:  ## run precommit quality checks
	bundle exec overcommit --run

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

bake:
	cookiecutter $(BAKE_OPTIONS) . --overwrite-if-exists

watch: bake
	watchmedo shell-command -p '*.*' -c 'make bake -e BAKE_OPTIONS=$(BAKE_OPTIONS)' -W -R -D \cookiecutter-pypackage/

replay: BAKE_OPTIONS=--replay
replay: watch
	;
