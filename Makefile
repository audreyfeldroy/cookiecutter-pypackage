BAKE_OPTIONS=--no-input

help:
	@echo "bake 	Generate project using defaults"
	@echo "help 	Show this help"
	@echo "test 	Run the tests"
	@echo "replay 	Replay last cookiecutter run and watch for changes"
	@echo "watch 	Generate project using defaults and watch for changes"
	

bake:  # Generate project using defaults
	cookiecutter $(BAKE_OPTIONS) . --overwrite-if-exists

watch: bake
	watchmedo shell-command -p '*.*' -c 'make bake -e BAKE_OPTIONS=$(BAKE_OPTIONS)' -W -R -D \{{cookiecutter.project_slug}}/

replay: BAKE_OPTIONS=--replay
replay: watch
	;


MAKECMDGOALS ?= .    

test:  ## Run all the tests, but allow for arguments to be passed
	@echo "Running with arg: $(filter-out $@,$(MAKECMDGOALS))"
	pytest $(filter-out $@,$(MAKECMDGOALS))

pdb:  ## Run all the tests, but on failure, drop into the debugger
	@echo "Running with arg: $(filter-out $@,$(MAKECMDGOALS))"
	pytest --pdb --maxfail=10 --pdbcls=IPython.terminal.debugger:TerminalPdb $(filter-out $@,$(MAKECMDGOALS))

%:
	@:	

build:  ## Build the project, useful for checking that packaging is correct
	rm -rf build
	rm -rf dist
	uv build

VERSION=v$(shell grep -m 1 version pyproject.toml | tr -s ' ' | tr -d '"' | tr -d "'" | cut -d' ' -f3)

version:  ## Print the current version of the project
	@echo "Current version is $(VERSION)"

tag:  ## Tag the current version in git and put to github
	echo "Tagging version $(VERSION)"
	git tag -a $(VERSION) -m "Creating version $(VERSION)"
	git push origin $(VERSION)	

clean:  ## Run all the formatting, linting, and testing commands
	ruff format .
	ruff check . --fix
	ruff check --select I --fix .
	pytest