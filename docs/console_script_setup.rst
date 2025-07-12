.. _console-script-setup:


Console Script Setup
=================

Optionally, your package can include a console script using Click or argparse (Python 3.2+).

How It Works
------------

If the 'command_line_interface' option is set to ['click'] or ['argparse'] during setup, cookiecutter will
add a file 'cli.py' in the project_slug subdirectory. An entry point is added to
setup.py that points to the main function in cli.py.

Usage
------------
To use the console script in development:

.. code-block:: bash

    pip install -e projectdir

'projectdir' should be the top level project directory with the setup.py file

The script will be generated with output for no arguments and --help.

--help
    show help menu and exit

Known Issues
------------
Using Click, installing the project in a development environment using:

.. code-block:: bash

    python setup.py develop

will not set up the entry point correctly. This is a known issue with Click.
The following will work as expected:

.. code-block:: bash

    python setup.py install
    pip install mypackage

With 'mypackage' adjusted to the specific project.


More Details
------------

You can read more about Click at:
http://click.pocoo.org/
