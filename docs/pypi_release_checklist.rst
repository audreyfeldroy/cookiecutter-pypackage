PyPI Release Checklist
======================

Before Your First Release
-------------------------

#. Register the package on PyPI:

    .. code-block:: bash

        python setup.py register

#. Visit PyPI to make sure it registered.

For Every Release
-------------------

#. Update HISTORY.rst

#. Commit the changes:

    .. code-block:: bash

        git add HISTORY.rst
        git commit -m "Changelog for upcoming release 0.1.1."

#. Update version number (can also be patch or major)

    .. code-block:: bash

        bumpversion minor

# Install the package again for local development, but with the new version number:

    .. code-block:: bash

        python setup.py develop

#. Run the tests:

    .. code-block:: bash

        tox

#. Release on PyPI by uploading both sdist and wheel:

    .. code-block:: bash

        python setup.py sdist upload
        python setup.py bdist_wheel upload

#. Push: git push

#. Push tags: git push --tags

#. Check the PyPI listing page to make sure that the README, release notes, and roadmap display properly. If not, try one of these:

#. Copy and paste the RestructuredText into http://rst.ninjs.org/ to find out what broke the formatting.

#. Check your long_description locally:

    .. code-block:: bash

        pip install readme_renderer
        python setup.py check -r -s

#. Edit the release on GitHub (e.g. https://github.com/audreyr/cookiecutter/releases). Paste the release notes into the release's release page, and come up with a title for the release.

For Every Release (Extended Version)
-------------------------------------

This version of the checklist is for extra-careful people who want to minimize their risk of release problems.

#. Update HISTORY.rst

#. Commit the changes:

    .. code-block:: bash

        git add HISTORY.rst
        git commit -m "Changelog for upcoming release 0.1.1."

#. Update version number (can also be patch or major)

    .. code-block:: bash

        bumpversion minor

# Install the package again for local development, but with the new version number:

    .. code-block:: bash

        python setup.py develop

#. Run the tests:

    .. code-block:: bash

        tox

#. Release on PyPI by uploading both sdist and wheel:

    .. code-block:: bash

        python setup.py sdist upload
        python setup.py bdist_wheel upload

#. Test that it pip installs:

    .. code-block:: bash

        mktmpenv
        pip install my_project
        <try out my_project>
        deactivate

#. Push: git push

#. Push tags: git push --tags

#. Check the PyPI listing page to make sure that the README, release notes, and roadmap display properly. If not, try one of these:

#. Copy and paste the RestructuredText into http://rst.ninjs.org/ to find out what broke the formatting.

#. Check your long_description locally:

    .. code-block:: bash

        pip install readme_renderer
        python setup.py check -r -s

#. Edit the release on GitHub (e.g. https://github.com/audreyr/cookiecutter/releases). Paste the release notes into the release's release page, and come up with a title for the release.
