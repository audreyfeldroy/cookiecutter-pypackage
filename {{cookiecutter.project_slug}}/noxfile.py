"""nox config file."""
import argparse
import os
import pathlib

import nox

# It's a good idea to keep your dev session out of the default list
# so it's not run twice accidentally
nox.options.sessions = ["test", "lint"]  # Sessions other than 'dev'

# this VENV_DIR constant specifies the name of the dir that the `dev`
# session will create, containing the virtualenv;
# the `resolve()` makes it portable
VENV_DIR = pathlib.Path("./.venv").resolve()


@nox.session
def dev(session: nox.Session) -> None:
    """
    Set up a python development environment for the project.

    This session will:
    - Create a python virtualenv for the session
    - Install the `virtualenv` cli tool into this environment
    - Use `virtualenv` to create a global project virtual environment
    - Invoke the python interpreter from the global project environment to install
      the project and all it's development dependencies.
    """
    session.install("virtualenv")
    # the VENV_DIR constant is explained above
    session.run("virtualenv", os.fsdecode(VENV_DIR), silent=True)

    python = os.fsdecode(VENV_DIR.joinpath("bin/python"))

    # Use the venv's interpreter to install the project along with
    # all it's dev dependencies, this ensures it's installed in the right way
    session.run(python, "-m", "pip", "install", "-e", ".[dev]", external=True)


@nox.session
def release(session: nox.Session) -> None:
    """
    Kicks off an automated release process by creating and pushing a new tag.

    Invokes bump2version with the posarg setting the version.

    Usage:
    $ nox -s release -- [major|minor|patch]
    """
    parser = argparse.ArgumentParser(description="Release a semver version.")
    parser.add_argument(
        "version",
        type=str,
        nargs=1,
        help="The type of semver release to make.",
        choices={"major", "minor", "patch"},
    )
    args: argparse.Namespace = parser.parse_args(args=session.posargs)
    version: str = args.version.pop()

    # If we get here, we should be good to go
    # Let's do a final check for safety
    confirm = input(
        f"You are about to bump the {version!r} version. Are you sure? [y/n]: "
    )

    # Abort on anything other than 'y'
    if confirm.lower().strip() != "y":
        session.error(f"You said no when prompted to bump the {version!r} version.")

    session.install("bump-my-version")

    session.log(f"Bumping the {version!r} version")
    session.run("bump-my-version", "bump", version)

    session.log("Pushing the new tag")
    session.run("git", "push", external=True)
    session.run("git", "push", "--tags", external=True)


@nox.session
def test(session: nox.Session) -> None:
    """
    Run the test suite.

    Usage:
    $ nox -s tests
    """
    session.install("pytest")
    session.run("pytest")


@nox.session
def lint(session: nox.Session) -> None:
    """
    Run linters.

    Usage:
    $ nox -s lint
    """
    session.install("ruff")
    session.run("ruff", "check")
