# PyPI Release Checklist

## Before Your First Release

1. Register the package on PyPI:

    ```bash
    python setup.py register
    ```

2. Visit PyPI to make sure it registered.

## For Every Release

1. Update `HISTORY.md`
2. Commit the changes:

    ```bash
    git add HISTORY.md
    git commit -m "Changelog for upcoming release 0.1.1."
    ```

3. Update version number (can also be minor or major):

    ```bash
    uv version --bump patch
    ```

4. Install the package again for local development, but with the new version number:

    ```bash
    python setup.py develop
    ```

5. Run the tests:

    ```bash
    tox
    ```

6. Push the commit:

    ```bash
    git push
    ```

7. Push the tags, creating the new release on both GitHub and PyPI:

    ```bash
    git push --tags
    ```

8. Check the PyPI listing page to make sure that the README, release notes, and roadmap display properly. If not, try one of these:
    - Copy and paste the Markdown into a Markdown previewer (such as https://dillinger.io/) to find out what broke the formatting.
