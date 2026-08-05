# PyPI Release Checklist

## First-Time Setup (One-Time)

1. Create a PyPI account at [pypi.org](https://pypi.org) if you don't have one.

2. Go to your PyPI account > Publishing > Add a new pending publisher.

3. Fill in the form:
   - **PyPI Project Name:** Your package name (e.g., `my-package`)
   - **Owner:** Your GitHub username or organization
   - **Repository name:** Your repo name
   - **Workflow name:** `publish.yml`
   - **Environment name:** `pypi`

4. If you opted into successful GitHub setup, the post-generation hook created
   the `pypi` environment. Otherwise, go to Settings > Environments > New
   environment and name it `pypi`. Optionally add required reviewers and
   restrict deployment to `v*` tags.

5. Run `just release` to trigger the publish (see below).

## During Development

Record user-visible changes in `CHANGELOG/unreleased.md` as they merge to
`main`. Keep versioned changelog files reserved for releases.

## Every Release

1. Bump the version and commit it:

    ```bash
    uv version patch  # or: minor, major
    git add pyproject.toml uv.lock
    git commit -m "Bump version to X.Y.Z"
    ```

2. Run the release command:

    ```bash
    just release
    ```

   `just release` moves `CHANGELOG/unreleased.md` to
   `CHANGELOG/X.Y.Z.md`, creates a fresh unreleased file, commits and pushes
   that release-notes commit, then creates and pushes the `vX.Y.Z` tag.

3. GitHub Actions builds, signs with Sigstore, and publishes to PyPI
   automatically.

Older generated projects that already contain only
`CHANGELOG/X.Y.Z.md` remain compatible with `just release`.

## Release Recovery

If release preparation fails before the tag is created, inspect the working
tree and finish or revert the release-notes commit before retrying. Never reuse
or overwrite an existing tag.

## Troubleshooting

If the publish fails:

- Check that your PyPI trusted publisher settings match your workflow exactly
- Verify the tag format matches what PyPI expects (e.g., `v1.0.0`)
- Look at the GitHub Actions logs for detailed error messages
