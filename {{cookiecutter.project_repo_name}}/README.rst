{{ cookiecutter.project_name }}
===============================

.. image:: https://img.shields.io/badge/docs-latest-brightgreen.svg
   :target: http://{{ cookiecutter.project_slug }}.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://travis-ci.org/{{ cookiecutter.github_username }}/{{ cookiecutter.project_repo_name }}.svg?branch=master
   :target: https://travis-ci.org/{{ cookiecutter.github_username }}/{{ cookiecutter.project_repo_name }}
   :alt: Travis Build

.. image:: https://img.shields.io/github/license/{{ cookiecutter.github_username }}/{{ cookiecutter.project_repo_name }}.svg
    :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_repo_name }}/blob/master/LICENSE.txt
    :alt: GitHub license

.. image:: https://badges.gitter.im/bird-house/birdhouse.svg
    :target: https://gitter.im/bird-house/birdhouse?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
    :alt: Join the chat at https://gitter.im/bird-house/birdhouse


{{ cookiecutter.project_name }} (the bird)
  *{{ cookiecutter.project_name }} is a bird ...*

{{ cookiecutter.project_short_description }}

* Free software: {{ cookiecutter.open_source_license }}
* Documentation: https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io.

Credits
-------

This package was created with Cookiecutter_ and the `bird-house/cookiecutter-birdhouse`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`bird-house/cookiecutter-birdhouse`: https://github.com/bird-house/cookiecutter-birdhouse
