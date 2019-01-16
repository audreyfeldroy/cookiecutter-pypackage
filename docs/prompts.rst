Prompts
=======

When you create a package, you are prompted to enter these values.

Templated Values
----------------

The following appear in various parts of your generated project.

full_name
    Your full name.

email
    Your email address.

github_username
    Your GitHub username.

project_name
    The name of your new Python package project. This is used in documentation, so spaces and any characters are fine here.
    
project_slug
    The namespace of your Python package. This should be Python import-friendly. Typically, it is the slugified version of project_name.

project_short_description
    A 1-sentence description of what your Python package does.

version
    The starting version number of the package.

Options
-------

command_line_interface
    Whether to create a console script using Click. Console script entry point will match the project_slug. Options: ['Click', "No command-line interface"]

license
    License of the project. Options ['MCH', 'MIT']
