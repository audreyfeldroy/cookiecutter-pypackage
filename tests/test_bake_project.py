import datetime
import importlib.util
import json
import shlex
import subprocess
import sys
import tarfile
import tomllib

import pytest


def run_inside_dir(command, dirpath):
    """Run a command from inside a given directory, raising on non-zero exit."""
    return subprocess.check_call(shlex.split(command), cwd=dirpath)


def check_output_inside_dir(command, dirpath):
    """Run a command from inside a given directory, returning the command output."""
    return subprocess.check_output(shlex.split(command), cwd=dirpath)


def test_year_compute_in_license_file(cookies):
    result = cookies.bake()
    assert result.exit_code == 0
    license_file = result.project_path / "LICENSE"
    now = datetime.datetime.now()
    assert str(now.year) in license_file.read_text()


def test_bake_with_defaults(cookies):
    result = cookies.bake()
    assert result.project_path.is_dir()
    assert result.exit_code == 0
    assert result.exception is None
    found_toplevel_files = [f.name for f in result.project_path.iterdir()]
    assert "src" in found_toplevel_files
    assert "tests" in found_toplevel_files


def test_bake_starts_with_an_unreleased_changelog(cookies):
    """Generated projects keep work-in-progress notes separate from releases."""
    result = cookies.bake(extra_context={"first_version": "1.2.3"})

    assert result.exit_code == 0
    changelog = result.project_path / "CHANGELOG"
    assert (changelog / "unreleased.md").is_file()
    assert not (changelog / "1.2.3.md").exists()


def test_baked_release_script_runs_the_release_lifecycle(cookies, monkeypatch):
    """The rendered release script finalizes notes and synchronizes main before tagging."""
    result = cookies.bake()
    assert result.exit_code == 0

    script_path = result.project_path / "scripts" / "release.py"
    spec = importlib.util.spec_from_file_location("baked_release_script", script_path)
    assert spec is not None
    assert spec.loader is not None
    release = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(release)

    commands = []
    monkeypatch.chdir(result.project_path)
    monkeypatch.setattr(release, "_ensure_clean_worktree", lambda: None)
    monkeypatch.setattr(release, "_ensure_release_branch", lambda: None)
    monkeypatch.setattr(release, "_ensure_tag_state", lambda tag: release.TagState(False, False))
    monkeypatch.setattr(release, "_github_release_exists", lambda tag: False)
    monkeypatch.setattr(release, "_run", lambda *command: commands.append(command))

    assert release.main() == 0

    notes_path = result.project_path / "CHANGELOG" / "0.1.0.md"
    assert notes_path.exists()
    assert (result.project_path / "CHANGELOG" / "unreleased.md").read_text(
        encoding="utf-8"
    ) == release.UNRELEASED_TEMPLATE
    assert ("git", "push", "origin", "HEAD:main") in commands


def test_bake_and_run_tests(cookies):
    result = cookies.bake()
    assert result.project_path.is_dir()
    run_inside_dir("uv run pytest", str(result.project_path))


def test_bake_and_run_ruff(cookies):
    """Baked project passes ruff linting and formatting out of the box."""
    result = cookies.bake()
    assert result.project_path.is_dir()
    run_inside_dir("uv run ruff check .", str(result.project_path))
    run_inside_dir("uv run ruff format --check .", str(result.project_path))


def test_bake_withspecialchars_and_run_tests(cookies):
    """Ensure that a `full_name` with double quotes does not break pyproject.toml"""
    result = cookies.bake(extra_context={"full_name": 'name "quote" name'})
    assert result.project_path.is_dir()
    assert result.exit_code == 0
    run_inside_dir("uv run pytest", str(result.project_path))


def test_bake_with_apostrophe_and_run_tests(cookies):
    """Ensure that a `full_name` with apostrophes does not break pyproject.toml"""
    result = cookies.bake(extra_context={"full_name": "O'connor"})
    assert result.project_path.is_dir()
    run_inside_dir("uv run pytest", str(result.project_path))


@pytest.mark.parametrize(
    "description",
    [
        'A "quoted" description',
        "A multiline\ndescription",
        "A path ending in a backslash \\",
    ],
)
def test_bake_preserves_description_in_valid_toml(cookies, description):
    """Descriptions with TOML-sensitive characters remain valid and unchanged."""
    result = cookies.bake(extra_context={"project_short_description": description})
    assert result.project_path.is_dir()
    assert result.exit_code == 0
    with (result.project_path / "pyproject.toml").open("rb") as pyproject_file:
        pyproject = tomllib.load(pyproject_file)
    assert pyproject["project"]["description"] == description


def test_bake_builds_when_package_and_import_names_differ(cookies):
    """Hatchling packages the configured import directory without guessing."""
    result = cookies.bake(
        extra_context={
            "package_name": "distribution-name",
            "import_name": "importable_name",
        }
    )
    assert result.exit_code == 0
    run_inside_dir("uv build", str(result.project_path))
    assert (result.project_path / "dist" / "distribution_name-0.1.0-py3-none-any.whl").is_file()


def test_bake_excludes_documentation_cache_from_sdist(cookies):
    """Local Zensical cache files never leak into a published source archive."""
    result = cookies.bake()
    assert result.exit_code == 0
    cache_dir = result.project_path / ".cache"
    cache_dir.mkdir()
    (cache_dir / "local-docs-cache").write_text("not package data\n", encoding="utf-8")

    run_inside_dir("uv build", str(result.project_path))

    sdist_path = next((result.project_path / "dist").glob("*.tar.gz"))
    with tarfile.open(sdist_path, "r:gz") as sdist:
        members = sdist.getnames()
    assert not any("/.cache/" in f"/{member}/" for member in members)


def test_bake_treats_import_name_as_data(cookies, tmp_path):
    """Python-shaped import names are validated without being executed."""
    marker = tmp_path / "import-name-was-executed"
    import_name = f'"; __import__("pathlib").Path({json.dumps(str(marker))}).touch(); module_name = "valid'

    result = cookies.bake(extra_context={"import_name": import_name})

    assert result.exit_code != 0
    assert not marker.exists()


@pytest.mark.skipif(sys.platform == "win32", reason="justfile not supported on Windows")
def test_just_quality_recipes(cookies):
    result = cookies.bake()
    project_path = str(result.project_path)
    output = check_output_inside_dir("just list", project_path)

    assert b"Show available commands" in output
    assert b"fix" in output
    assert b"check" in output
    assert b"fix-and-check" in output
    assert b"\n    ci " not in output

    run_inside_dir("just fix", project_path)
    run_inside_dir("just check", project_path)
    run_inside_dir("just fix-and-check", project_path)


def test_py_typed_marker_exists(cookies):
    """Verify generated package includes a py.typed marker file (PEP 561)."""
    result = cookies.bake()
    assert result.exit_code == 0
    import_name = result.project_path.name.lower().replace("-", "_")
    assert (result.project_path / "src" / import_name / "py.typed").is_file()


def test_typing_classifier_in_pyproject(cookies):
    """Verify generated pyproject.toml includes the Typing :: Typed classifier."""
    result = cookies.bake()
    assert result.exit_code == 0
    content = (result.project_path / "pyproject.toml").read_text()
    assert '"Typing :: Typed"' in content


def test_baked_workflows_support_private_repositories(cookies):
    """Checkout and security workflows use safe private-repository defaults."""
    result = cookies.bake()
    assert result.exit_code == 0
    workflows = result.project_path / ".github" / "workflows"

    ci = (workflows / "ci.yml").read_text()
    assert ci.count("contents: read") == 4

    publish = (workflows / "publish.yml").read_text()
    build_job = publish.split("  publish:", maxsplit=1)[0]
    assert "contents: read" in build_job

    codeql = (workflows / "codeql.yml").read_text()
    private_code_security_opt_in = (
        "${{ github.event.repository.private == false || vars.CODE_SECURITY_ENABLED == 'true' }}"
    )
    assert private_code_security_opt_in in codeql
    assert "actions: read" in codeql
    assert "contents: read" in codeql

    zizmor = (workflows / "zizmor.yml").read_text()
    assert f"advanced-security: {private_code_security_opt_in}" in zizmor
    assert "actions: read" in zizmor
    assert "contents: read" in zizmor

    docs = (workflows / "docs.yml").read_text()
    assert "${{ vars.DOCS_DEPLOYMENT_ENABLED == 'true' }}" in docs
