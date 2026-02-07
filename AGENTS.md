# Agent Instructions

## Keep the outer repo in sync with the generated project

This repo has two layers: the outer repo (the cookiecutter template project itself) and the generated project (inside `{{cookiecutter.pypi_package_name}}/`). They share similar patterns for pyproject.toml, justfile, CI workflows, etc.

When you fix or change something in the generated project template, check whether the same fix applies to the outer repo. If it does, make both changes together. Don't leave the outer repo behind.
