.. _configuration:

Configuration
=============

Command-line options
--------------------

You can overwrite the default `PyWPS`_ configuration by using command-line options.
See the {{ cookiecutter.project_name }} help which options are available::

    $ {{ cookiecutter.project_slug }} --help
    --hostname HOSTNAME        hostname in PyWPS configuration.
    --port PORT                port in PyWPS configuration.

Start service with different hostname and port::

    $ {{ cookiecutter.project_slug }} --hostname localhost --port 5001

Use a custom configuration file
-------------------------------

You can overwrite the default `PyWPS`_ configuration by providing your own
PyWPS configuration file (just modifiy the options you want to change).
Use one of the existing ``sample-*.cfg`` files as example and copy them to ``etc/custom.cfg``.

For example change the hostname (*demo.org*) and logging level:

.. code-block:: sh

   $ cd {{ cookiecutter.project_slug }}
   $ vim etc/custom.cfg
   $ cat etc/custom.cfg
   [server]
   url = http://demo.org:{{ cookiecutter.http_port }}/wps
   outputurl = http://demo.org:{{ cookiecutter.http_port }}/outputs

   [logging]
   level = DEBUG

Start the service with your custom configuration:

.. code-block:: sh

   # start the service with this configuration
   $ {{ cookiecutter.project_slug }} -c etc/custom.cfg


.. _PyWPS: http://pywps.org/
