#!/usr/bin/env python
import pathlib

if __name__ == "__main__":
    if "{{ cookiecutter.create_author_file }}" != "y":
        pathlib.Path("AUTHORS.md").unlink()
        pathlib.Path("docs", "authors.md").unlink()
