def test_import_{{ cookiecutter.project_slug }}():
    try:
        import {{ cookiecutter.project_slug }}           # noqa
    except ImportError:
        assert False
