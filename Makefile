COOKIES_DIR=$(CURDIR)/cookies
BAKE_OPTIONS=--no-input --output-dir $(COOKIES_DIR)

.DEFAULT_GOAL := all

.PHONY: all
all: help

.PHONY: help
help:
	@echo "bake 	to generate project using defaults"
	@echo "test 	to test cookiecutter template generation"
	@echo "clean 	to remove baked cookies"
	@echo "docs   to generate Sphinx docs"

.PHONY: test
test:
	@echo "Running all tests"
	pytest

.PHONY: clean
clean:
	test -d $(COOKIES_DIR) && rm -v -rf $(COOKIES_DIR);

.PHONY: bake
bake:
	cookiecutter $(BAKE_OPTIONS) . --overwrite-if-exists

.PHONY: docs
docs:
	@echo "Generating docs with Sphinx ..."
	$(MAKE) -C $@ html
	@echo "open your browser: open docs/build/html/index.html"

# generate project using defaults and watch for changes
# watch: bake
# 	watchmedo shell-command -p '*.*' -c 'make bake -e BAKE_OPTIONS=$(BAKE_OPTIONS)' -W -R -D \{{cookiecutter.project_slug}}/
#
# replay last cookiecutter run and watch for changes
# replay: BAKE_OPTIONS=--replay
# replay: watch
# 	;
