.. _installation:

Installation
============

The installation is using the Python distribution system `Anaconda`_ to maintain software dependencies.
Anaconda will be installed during the installation process in your home directory ``~/anaconda``.

The installation process setups a conda environment named ``{{ cookiecutter.project_slug }}`` with all dependent conda (and pip) packages.
The installation folder (for configuration files etc) is by default ``~/birdhouse``.
Configuration options can be overriden in the buildout ``custom.cfg`` file. The ``ANACONDA_HOME`` and ``CONDA_ENVS_DIR`` locations
can be changed in the ``Makefile.config`` file.

The default installation *does not need admin rights* and files will only be written into the ``$HOME`` folder of the installation user.
The services are started using `supervisor <http://supervisord.org/>`_ and run as the installation user.

Now, check out the {{ cookiecutter.project_slug }} code from GitHub and start the installation:

.. code-block:: sh

   $ git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
   $ cd {{ cookiecutter.project_slug }}
   $ make clean install

After successful installation you need to start the services:

.. code-block:: sh

   $ make start  # starts supervisor services
   $ make status # shows supervisor status

The depolyed WPS service is by default available on http://localhost:{{ cookiecutter.http_port }}/wps?service=WPS&version=1.0.0&request=GetCapabilities.

Check the log files for errors:

.. code-block:: sh

   $ tail -f  ~/birdhouse/var/log/pywps/{{ cookiecutter.project_slug }}.log
   $ tail -f  ~/birdhouse/var/log/supervisor/{{ cookiecutter.project_slug }}.log

You will find more information about the installation in the `Makefile documentation <http://birdhousebuilderbootstrap.readthedocs.io/en/latest/>`_.

Non-default installation
------------------------

You can customize the installation to use different ports, locations and run user.

To change the anaconda location edit the ``Makefile.config``, for example::

   ANACONDA_HOME ?= /opt/anaconda
   CONDA_ENVS_DIR ?= /opt/anaconda/envs

You can install {{ cookiecutter.project_slug }} as ``root`` and run it as unprivileged user like ``www-data``:

.. code-block:: sh

   root$ mkdir -p /opt/birdhouse/src
   root$ cd /opt/birdhouse/src
   root$ git clone https://github.com/bird-house/{{ cookiecutter.project_slug }}.git
   root$ cd {{ cookiecutter.project_slug }}

Edit ``custom.cfg``:

.. code-block:: ini

    [buildout]
    extends = buildout.cfg

    [settings]
    hostname = {{ cookiecutter.project_slug }}
    http-port = 80
    output-port = 8000
    log-level = WARN

    # deployment options
    prefix = /opt/birdhouse
    user = www-data
    etc-user = root

Run the installtion and start the services:

.. code-block:: sh

    root$ make clean install
    root$ make start      # stop or restart
    root$ make status

.. _Anaconda: https://www.continuum.io/
