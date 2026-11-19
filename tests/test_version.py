"""Tests for package version metadata."""

from importlib.metadata import version

import cookiecutter_pypackage


def test_package_version_matches_distribution_metadata():
    """The public package version comes from the authoritative metadata."""
    assert cookiecutter_pypackage.__version__ == version("cookiecutter-pypackage")
