.. _console-script-setup:


Console Script Setup
=================

Optionally, your package can include a console script using argparse.

How It Works
------------

If the 'command_line_interface' option is set to ['argparse'] during setup, cookiecutter will
add a file 'cli.py' in the package_name subdirectory. An entry point is added to
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
