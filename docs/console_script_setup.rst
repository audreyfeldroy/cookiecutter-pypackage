.. _console-script-setup:


Console Script Setup
=================

Optionally, your package can include a console script using Click or argparse (Python 3.2+).

How It Works
------------

If the 'command_line_interface' option is set to ['click'] or ['argparse'] during setup, cookiecutter will
add a file 'cli.py' in the project_slug subdirectory. An entry point is added to
pyproject.toml that points to the main function in cli.py.

Usage
------------
To use the console script in development:

.. code-block:: bash

    pip install -e projectdir

'projectdir' should be the top level project directory with the pyproject.toml file

The script will be generated with output for no arguments and --help.

--help
    show help menu and exit

More Details
------------

You can read more about Click at:
http://click.pocoo.org/
