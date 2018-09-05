.. _installation:

Installation
============

.. contents::
    :local:
    :depth: 1

Install from Conda
------------------

.. warning::

   TODO: Prepare Conda package.

Install from GitHub
-------------------

Check out code from the {{ cookiecutter.project_name }} GitHub repo and start the installation:

.. code-block:: sh

   $ git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_repo_name }}.git
   $ cd {{ cookiecutter.project_slug }}
   $ conda env create -f environment.yml
   $ source activate {{ cookiecutter.project_slug }}
   $ python setup.py develop

... or do it the lazy way
+++++++++++++++++++++++++

The previous installation instructions assume you have Anaconda installed.
We provide also a ``Makefile`` to run this installation without additional steps:

.. code-block:: sh

   $ git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_repo_name }}.git
   $ cd {{ cookiecutter.project_slug }}
   $ make clean    # cleans up a previous Conda environment
   $ make install  # installs Conda if necessary and runs the above installation steps

Start {{ cookiecutter.project_name }} PyWPS service
-{{ '-' * (cookiecutter.project_name|count + 19) }}

After successful installation you can start the service using the ``{{ cookiecutter.project_slug }}`` command-line.

.. code-block:: sh

   $ {{ cookiecutter.project_slug }} --help # show help
   $ {{ cookiecutter.project_slug }} start  # start service with default configuration

   OR

   $ {{ cookiecutter.project_slug }} start --daemon # start service as daemon
   loading configuration
   forked process id: 42

The deployed WPS service is by default available on:

http://localhost:{{ cookiecutter.http_port }}/wps?service=WPS&version=1.0.0&request=GetCapabilities.

.. NOTE:: Remember the process ID (PID) so you can stop the service with ``kill PID``.

You can find which process uses a given port using the following command (here for port 5000):

.. code-block:: sh

   $ netstat -nlp | grep :5000


Check the log files for errors:

.. code-block:: sh

   $ tail -f  pywps.log

... or do it the lazy way
+++++++++++++++++++++++++

You can also use the ``Makefile`` to start and stop the service:

.. code-block:: sh

  $ make start
  $ make status
  $ tail -f pywps.log
  $ make stop


Run {{ cookiecutter.project_name }} as Docker container
-{{ '-' * (cookiecutter.project_name|count + 23) }}

You can also run {{ cookiecutter.project_name }} as a Docker container.

.. warning::

  TODO: Describe Docker container support.

Use Ansible to deploy {{ cookiecutter.project_name }} on your System
-{{ '-' * (cookiecutter.project_name|count + 36) }}

Use the `Ansible playbook`_ for PyWPS to deploy {{ cookiecutter.project_name }} on your system.


.. _Ansible playbook: http://ansible-wps-playbook.readthedocs.io/en/latest/index.html
