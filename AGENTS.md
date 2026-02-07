# Agent Instructions

## Keep the outer repo in sync with the generated project

This repo has two layers: the outer repo (the cookiecutter template project itself) and the generated project (inside `{{cookiecutter.pypi_package_name}}/`). They share similar patterns for pyproject.toml, justfile, CI workflows, etc.

When you fix or change something in the generated project template, check whether the same fix applies to the outer repo. If it does, make both changes together. Don't leave the outer repo behind.

## Merging community PRs

- Before merging, study the PR carefully with BDFL Audrey and give her your thoughts. Only merge after human approval.
- When merging a PR from an external contributor, leave a comment thanking them after the merge is complete. Not before.
- If a PR needs rebasing, check out the branch, rebase, and push back to the contributor's fork so the PR shows green on GitHub.
- If the contributor's fork is archived or inaccessible, open a new PR from origin with the rebased branch. Credit the original author (preserve their commit authorship) and explain in the PR body and a comment on the original PR why a new one was needed.

## Commits

Keep commits small and atomic. One logical change per commit. Don't bundle unrelated changes.

## Read the actual files

- Always read `cookiecutter.json` before constructing commands or examples that reference template variables.
- Don't trust your training data for project-specific details (config files, schemas, specs). Read the actual file, because your memory of it may be stale or wrong.
