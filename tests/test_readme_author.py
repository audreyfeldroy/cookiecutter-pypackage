"""Tests for README author attribution rendering."""


def test_readme_created_by_without_website(cookies):
    """With no author_website, name links to GitHub profile."""
    result = cookies.bake(
        extra_context={
            "package_name": "attr-test",
            "full_name": "Audrey M. Roy Greenfeld",
            "github_username": "audreyfeldroy",
            "pypi_username": "audreyfeldroy",
            "author_website": "",
        },
    )
    assert result.exit_code == 0
    readme = (result.project_path / "README.md").read_text()

    # Name links to GitHub when no website provided
    assert "[Audrey M. Roy Greenfeld](https://github.com/audreyfeldroy)" in readme

    # GitHub repo link in navigation line
    assert "[GitHub](https://github.com/audreyfeldroy/attr-test/)" in readme

    # GitHub profile should NOT appear in Created by (name already links there)
    created_by = [line for line in readme.splitlines() if "Created by" in line][0]
    assert "[@audreyfeldroy](https://github.com/audreyfeldroy)" not in created_by

    # PyPI profile appears in Created by line
    assert "[@audreyfeldroy](https://pypi.org/user/audreyfeldroy/)" in created_by


def test_readme_created_by_with_website(cookies):
    """With author_website set, name links to website and GitHub gets a sub-bullet."""
    result = cookies.bake(
        extra_context={
            "package_name": "attr-test-site",
            "full_name": "Audrey M. Roy Greenfeld",
            "github_username": "audreyfeldroy",
            "author_website": "https://audrey.feldroy.com",
        },
    )
    assert result.exit_code == 0
    readme = (result.project_path / "README.md").read_text()

    # Name links to the website
    assert "[Audrey M. Roy Greenfeld](https://audrey.feldroy.com)" in readme

    # GitHub profile appears in Created by line (separate from the repo link bullet)
    created_by = [line for line in readme.splitlines() if "Created by" in line][0]
    assert "[@audreyfeldroy](https://github.com/audreyfeldroy)" in created_by


def test_readme_no_duplicate_links(cookies):
    """Links should appear in the top section only, not repeated in Author section."""
    result = cookies.bake(
        extra_context={
            "package_name": "dedup-test",
            "full_name": "Audrey M. Roy Greenfeld",
            "github_username": "audreyfeldroy",
        },
    )
    assert result.exit_code == 0
    readme = (result.project_path / "README.md").read_text()

    lines = readme.split("\n")
    author_idx = next(i for i, line in enumerate(lines) if line.strip() == "## Author")
    author_section = "\n".join(lines[author_idx:])

    # Author section has the prose line but no link bullets
    assert "Audrey M. Roy Greenfeld" in author_section
    assert "* " not in author_section.split("Built with")[0].split("## Author")[1]
