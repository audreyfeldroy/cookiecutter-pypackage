# Show available commands
list:
    @just --list

# Generate project using defaults
bake BAKE_OPTIONS="--no-input":  
    cookiecutter {{BAKE_OPTIONS}} . --overwrite-if-exists

# Watch template for changes and rebake automatically
dev:
    uv run python dev.py

# replay: BAKE_OPTIONS="--replay"
# replay: watch
# 	;



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

# Run all the tests, but allow for arguments to be passed
test *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run --python=3.13 pytest {{ARGS}}

# Run all the tests, but on failure, drop into the debugger
pdb *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run --python=3.13 --with pytest --with httpx pytest --pdb --maxfail=10 --pdbcls=IPython.terminal.debugger:TerminalPdb {{ARGS}}

# Run all the formatting, linting, type checking, and testing commands
qa:
    uv run --python=3.13 ruff format .
    uv run --python=3.13 ruff check . --fix
    uv run --python=3.13 ruff check --select I --fix .
    uv run --python=3.13 ty check .
    uv run --python=3.13 pytest .

# Run all the checks for CI
ci:
    uv run --python=3.13 ruff format --check .
    uv run --python=3.13 ruff check .
    uv run --python=3.13 ruff check --select I .
    uv run --python=3.13 ty check .
    uv run --python=3.13 pytest .

# Run all the tests for all the supported Python versions
testall:
    uv run --python=3.10 pytest
    uv run --python=3.11 pytest
    uv run --python=3.12 pytest
    uv run --python=3.13 pytest

# Run coverage, and build to HTML
coverage:
    uv run --python=3.13 coverage run -m pytest .
    uv run --python=3.13 coverage report -m
    uv run --python=3.13 coverage html

# Serve docs locally with live reload
docs-serve:
    -lsof -ti :8000 | xargs kill
    uv run --group docs zensical serve

# Build docs
docs-build:
    uv run --group docs zensical build --clean