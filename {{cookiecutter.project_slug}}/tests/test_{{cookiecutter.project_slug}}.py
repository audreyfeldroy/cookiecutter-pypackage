import pytest


def test_import_{{ cookiecutter.project_slug }}():
    try:
        import {{ cookiecutter.project_slug }}           # noqa
    except ImportError:
        pytest.fail('import {{ cookiecutter.project_slug }} failed')
