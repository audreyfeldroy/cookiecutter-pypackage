from typing import Any

import nox
from nox.sessions import Session

nox.options.default_venv_backend = "uv"


@nox.session(python=["3.10", "3.11", "3.12", "3.13"])  # type: ignore[misc]
def tests(session: Session) -> Any:
    """Run the test suite."""
    session.install(".[dev]")
    session.run("pytest")


@nox.session  # type: ignore[misc]
def ruff(session: Session) -> Any:
    """Lint with ruff."""
    session.install("ruff")
    session.run("ruff", "check", ".")
