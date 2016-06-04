help:
	@echo "bake 	generate project using defaults"
	@echo "watch 	generate project using defaults and watch for changes"

bake:
	cookiecutter --no-input . --overwrite-if-exists

watch: bake
	watchmedo shell-command -p '*.*' -c 'make bake' -W -R -D \{{cookiecutter.project_slug}}/
