"""
Post-Generation Python Hooks
"""

from pathlib import Path

REMOVE_PATHS = [
    "{% if cookiecutter.publish_to_pypi == 'False' and cookiecutter.publish_to_docker_hub == 'False' %} .github/workflows/publish.yaml {% endif %}",
]

for path in set(REMOVE_PATHS):
    path = path.strip()
    if path:
        path_obj = Path(path)
        if path_obj.exists() and path_obj.is_dir():
            path_obj.rmdir()
        elif path_obj.exists():
            path_obj.unlink()
