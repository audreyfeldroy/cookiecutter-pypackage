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

# Finalize release notes, tag, push, and create a GitHub release
release:
    uv run scripts/release.py

# Run all the tests, but allow for arguments to be passed
test *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run --python=3.14 pytest {{ARGS}}

# Run all the tests, but on failure, drop into the debugger
pdb *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run --python=3.14 pytest --pdb --maxfail=10 {{ARGS}}

# Apply automatic formatting and lint fixes
fix:
    uv run --python=3.14 ruff format .
    uv run --python=3.14 ruff check . --fix

# Verify formatting, linting, types, and tests on Python 3.14 without modifying source files
check:
    uv run --python=3.14 ruff format --check .
    uv run --python=3.14 ruff check .
    uv run --python=3.14 ty check .
    uv run --python=3.14 pytest

# Apply automatic fixes, then run the local quality gate
fix-and-check: fix check

# Compatibility alias for fix-and-check
qa: fix-and-check

# Compatibility alias for check
ci: check

# Run all the tests for all the supported Python versions
testall:
    uv run --python=3.12 pytest
    uv run --python=3.13 pytest
    uv run --python=3.14 pytest

# Run coverage, and build to HTML
coverage:
    uv run --python=3.14 coverage run -m pytest
    uv run --python=3.14 coverage report -m
    uv run --python=3.14 coverage html

# Serve docs locally with live reload
docs-serve:
    uv run --group docs zensical serve

# Build docs
docs-build:
    uv run --group docs zensical build --clean

# Remove all build, test, coverage and Python artifacts
clean: clean-build clean-pyc clean-test clean-bake

# Remove build artifacts
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

# Remove Python file artifacts
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

# Remove test and coverage artifacts
clean-test:
	rm -f .coverage
	rm -f .coverage.*
	rm -fr htmlcov/
	rm -fr .pytest_cache

# Remove baked project output
clean-bake:
	rm -fr python-boilerplate/
