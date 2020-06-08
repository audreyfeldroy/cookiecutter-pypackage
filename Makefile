BAKE_OPTIONS=--no-input

help:
	@echo "bake	generate project using defaults"
	@echo "watch	generate project using defaults and watch for changes"
	@echo "replay	replay last cookiecutter run and watch for changes"
	@echo "lint	check style with flake8 and black"
	@echo "fix	fix black and isort style violations"
	@echo "test	run tests quickly with the default Python"

bake:
	cookiecutter $(BAKE_OPTIONS) . --overwrite-if-exists

watch: bake
	watchmedo shell-command -p '*.*' -c 'make bake -e BAKE_OPTIONS=$(BAKE_OPTIONS)' -W -R -D \{{cookiecutter.project_repo}}/

replay: BAKE_OPTIONS=--replay
replay: watch
	;

lint:
	flake8 hooks tests setup.py
	black --check --diff hooks tests setup.py

fix:
	black hooks tests setup.py
	isort -rc hooks tests setup.py

test:
	pytest
