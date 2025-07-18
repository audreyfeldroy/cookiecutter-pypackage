import nox

nox.options.default_venv_backend = "uv"

@nox.session(python=["3.9", "3.10", "3.11", "3.12", "3.13"])
def tests(session):
    """Run the test suite."""
    session.install("-r", "requirements_dev.txt")
    session.run("pytest")

@nox.session
def ruff(session):
    """Lint with ruff."""
    session.install("ruff")
    session.run("ruff", "check", ".")
