.PHONY: clean test help quality
.DEFAULT_GOAL := default

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

default: test ## run default typechecking and tests

clean: ## remove all built artifacts

test: ## run tests quickly

quality:  ## run precommit quality checks
	bundle exec overcommit --run

update_from_cookiecutter: ## Bring in changes from template project used to create this repo
	IN_COOKIECUTTER_PROJECT_UPGRADER=1 cookiecutter_project_upgrader || true
	git checkout cookiecutter-template && git push && (git checkout main; bundle exec overcommit --sign)
	git checkout main && bundle exec overcommit --sign && git pull && (git checkout -b update-from-cookiecutter-$$(date +%Y-%m-%d-%H%M); bundle exec overcommit --sign)
	git merge cookiecutter-template || true
	@echo
	@echo "Please resolve any merge conflicts below and push up a PR with:"
	@echo
	@echo '   gh pr create --title "Update from cookiecutter" --body "Automated PR to update from cookiecutter boilerplate"'
	@echo
	@echo
