.. highlight:: shell

============
Installation
============


Stable release
--------------

To install {{ cookiecutter.project_name }}, run this command in your terminal:

.. code-block:: console

    $ pip install {{ cookiecutter.project_slug }}

This is the preferred method to install {{ cookiecutter.project_name }}, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for {{ cookiecutter.project_name }} can be downloaded from the `Github repo`_.

Option 1
^^^^^^^^
You can directly install it:

.. code-block:: console

    $ pip install git+https://github.com/MeteoSwiss-APN/{{ cookiecutter.project_slug }}#egg={{ cookiecutter.project_slug }}

or in developer mode:

.. code-block:: console

    $ pip install -e git+https://github.com/MeteoSwiss-APN/{{ cookiecutter.project_slug }}#egg={{ cookiecutter.project_slug }}

For furhter details see the `pip documentation`_.

Option 2
^^^^^^^^
You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _`pip documentation`: https://pip.pypa.io/en/stable/reference/pip_install/#vcs-support
.. _Github repo: https://github.com/MeteoSwiss-APN/{{ cookiecutter.project_slug }}
.. _tarball: https://github.com/MeteoSwiss-APN/{{ cookiecutter.project_slug }}/tarball/master
