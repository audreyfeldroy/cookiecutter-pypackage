COOKIES_DIR=$(CURDIR)/cookies
BAKE_OPTIONS=--no-input --output-dir $(COOKIES_DIR)


help:
	@echo "bake 	generate project using defaults"
	@echo "test 	test cookiecutter template generation"
	@echo "clean 	remove baked cookies"

test:
	pytest

clean:
	test -d $(COOKIES_DIR) && rm -v -rf $(COOKIES_DIR);

bake:
	cookiecutter $(BAKE_OPTIONS) . --overwrite-if-exists

# generate project using defaults and watch for changes
# watch: bake
# 	watchmedo shell-command -p '*.*' -c 'make bake -e BAKE_OPTIONS=$(BAKE_OPTIONS)' -W -R -D \{{cookiecutter.project_slug}}/
#
# replay last cookiecutter run and watch for changes
# replay: BAKE_OPTIONS=--replay
# replay: watch
# 	;
