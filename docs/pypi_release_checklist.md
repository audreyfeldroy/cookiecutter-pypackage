# PyPI Release Checklist

## First-Time Setup (One-Time)

1. Create a PyPI account at [pypi.org](https://pypi.org) if you don't have one.

2. Go to your PyPI account > Publishing > Add a new pending publisher.

3. Fill in the form:
   - **PyPI Project Name:** Your package name (e.g., `my-package`)
   - **Owner:** Your GitHub username or organization
   - **Repository name:** Your repo name
   - **Workflow name:** `publish.yml`
   - **Environment name:** Leave blank

4. Push your first tag to trigger the publish (see below).

## Every Release

1. Update `HISTORY.md` with your changes.

2. Bump version:

    ```bash
    uv version patch  # or: minor, major
    ```

3. Commit:

    ```bash
    git commit -am "Release X.Y.Z"
    ```

4. Tag and push:

    ```bash
    just tag
    ```

    Or manually:

    ```bash
    git tag vX.Y.Z
    git push origin vX.Y.Z
    ```

5. GitHub Actions publishes to PyPI automatically.

## Troubleshooting

If the publish fails:

- Check that your PyPI trusted publisher settings match your workflow exactly
- Verify the tag format matches what PyPI expects (e.g., `v1.0.0`)
- Look at the GitHub Actions logs for detailed error messages
