
# Generate project using defaults
bake BAKE_OPTIONS="--no-input":  
	cookiecutter {{BAKE_OPTIONS}} . --overwrite-if-exists

# Watch for changes
watch BAKE_OPTIONS="--no-input": bake
    watchmedo shell-command \
        -p '*.*' \
        -c 'just bake {{BAKE_OPTIONS}}' \
        -W -R -D {{'{{cookiecutter.project_slug}}'}}

# replay: BAKE_OPTIONS="--replay"
# replay: watch
# 	;


# Run all the tests, but allow for arguments to be passed
test *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run --python=3.13 --extra dev pytest {{ARGS}}

# Run all the tests, but on failure, drop into the debugger
pdb *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run --python=3.13 --with pytest --with httpx pytest --pdb --maxfail=10 --pdbcls=IPython.terminal.debugger:TerminalPdb {{ARGS}}



# Build the project, useful for checking that packaging is correct
build:
	rm -rf build
	rm -rf dist
	uv build

VERSION := `grep -m1 '^version' pyproject.toml | sed -E 's/version = "(.*)"/\1/'`

# Print the current version of the project
version:
    @echo "Current version is {{VERSION}}"

# Tag the current version in git and put to github
tag:
    echo "Tagging version v{{VERSION}}"
    git tag -a v{{VERSION}} -m "Creating version v{{VERSION}}"
    git push origin v{{VERSION}}

# Run all the formatting, linting, and testing commands
clean:  
	ruff format .
	ruff check . --fix
	ruff check --select I --fix .
	pytest