BAKE_OPTIONS=--no-input

help:
	@echo "bake 	generate project using defaults"
	@echo "watch 	generate project using defaults and watch for changes"
	@echo
	@echo "To replay last run, use:  make watch -e BAKE_OPTIONS=--replay"

bake:
	cookiecutter $(BAKE_OPTIONS) . --overwrite-if-exists

watch: bake
	watchmedo shell-command -p '*.*' -c 'make bake -e BAKE_OPTIONS=$(BAKE_OPTIONS)' -W -R -D \{{cookiecutter.project_slug}}/

watch-replay: BAKE_OPTIONS=--replay
watch-replay: watch
	;
