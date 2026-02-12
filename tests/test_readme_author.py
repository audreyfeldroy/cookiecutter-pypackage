"""Tests for README author attribution rendering."""

from contextlib import contextmanager

from cookiecutter.utils import rmtree


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project))


def test_readme_created_by_without_website(cookies):
    """With no author_website, name links to GitHub profile."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "pypi_package_name": "attr-test",
            "full_name": "Audrey M. Roy Greenfeld",
            "github_username": "audreyfeldroy",
            "pypi_username": "audreyfeldroy",
            "author_website": "",
        },
    ) as result:
        assert result.exit_code == 0
        readme = result.project.join("README.md").read()

        # Name links to GitHub when no website provided
        assert "**[Audrey M. Roy Greenfeld](https://github.com/audreyfeldroy)**" in readme

        # GitHub should NOT appear as a separate sub-bullet (it's already the name link)
        assert "GitHub: https://github.com/" not in readme

        # PyPI profile sub-bullet should still appear
        assert "PyPI: https://pypi.org/user/audreyfeldroy/" in readme


def test_readme_created_by_with_website(cookies):
    """With author_website set, name links to website and GitHub gets a sub-bullet."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "pypi_package_name": "attr-test-site",
            "full_name": "Audrey M. Roy Greenfeld",
            "github_username": "audreyfeldroy",
            "author_website": "https://audrey.feldroy.com",
        },
    ) as result:
        assert result.exit_code == 0
        readme = result.project.join("README.md").read()

        # Name links to the website
        assert "**[Audrey M. Roy Greenfeld](https://audrey.feldroy.com)**" in readme

        # GitHub appears as a separate sub-bullet
        assert "GitHub: https://github.com/audreyfeldroy" in readme


def test_readme_no_duplicate_links(cookies):
    """Links should appear in the top section only, not repeated in Author section."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "pypi_package_name": "dedup-test",
            "full_name": "Audrey M. Roy Greenfeld",
            "github_username": "audreyfeldroy",
        },
    ) as result:
        assert result.exit_code == 0
        readme = result.project.join("README.md").read()

        lines = readme.split("\n")
        author_idx = next(i for i, line in enumerate(lines) if line.strip() == "## Author")
        author_section = "\n".join(lines[author_idx:])

        # Author section has the prose line but no link bullets
        assert "Audrey M. Roy Greenfeld" in author_section
        assert "* " not in author_section.split("Built with")[0].split("## Author")[1]
