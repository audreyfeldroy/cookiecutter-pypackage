BAKE_OPTIONS=--no-input

all: test quality

test:
	pytest

quality:
	overcommit --run

help:
	@echo "bake 	generate project using defaults"
	@echo "watch 	generate project using defaults and watch for changes"
	@echo "replay 	replay last cookiecutter run and watch for changes"
	@echo "test 	run project tests"
	@echo "quality	run quality tools"

bake:
	cookiecutter $(BAKE_OPTIONS) . --overwrite-if-exists

watch: bake
	watchmedo shell-command -p '*.*' -c 'make bake -e BAKE_OPTIONS=$(BAKE_OPTIONS)' -W -R -D \{{cookiecutter.project_slug}}/

replay: BAKE_OPTIONS=--replay
replay: watch
	;

update_from_cookiecutter: ## Bring in changes from template project used to create this repo
	IN_COOKIECUTTER_PROJECT_UPGRADER=1 cookiecutter_project_upgrader || true
	git checkout cookiecutter-template && git push && (git checkout main; bundle exec overcommit --sign)
	git checkout main && bundle exec overcommit --sign && git pull && git checkout -b update-from-cookiecutter-$$(date +%Y-%m-%d-%H%M)
	git merge cookiecutter-template || true
	@echo
	@echo "Please resolve any merge conflicts below and push up a PR with:"
	@echo
	@echo '   gh pr create --title "Update from cookiecutter" --body "Automated PR to update from cookiecutter boilerplate"'
	@echo
	@echo
