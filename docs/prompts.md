# Prompts

When you create a package, you are prompted to enter these values.

## Templated Values

The following appear in various parts of your generated project.


## Templated Values

The following appear in various parts of your generated project.

<dl>
<dt>plugin_name</dt>
<dd>The base name of your plugin (without "NetBox" or "Plugin").  This is used
to initialize most of the other settings.</dd>

<dt>project_name</dt>
<dd>The name of your new Python package project. This is used in
documentation, so spaces and any characters are fine here.</dd>

<dt>project_slug</dt>
<dd>The name of your Python package for PyPI, also as the repository name of GitHub.
Typically, it is the slugified version of project_name.</dd>

<dt>project_short_description</dt>
<dd>A 1-sentence description of what your Python package does.</dd>

<dt>full_name</dt>
<dd>Your full name.</dd>

<dt>email</dt>
<dd>Your email address.</dd>

<dt>github_username</dt>
<dd>Your GitHub username.</dd>

<dt>version</dt>
<dd>The starting version number of the package.</dd>
</dl>

## Options

The following package configuration options set up different features
for your project.

<dl>
<dt>open_source_license</dt>
<dd>Choose a license. Options: [1. Apache-2.0, 2. MIT, 3. BSD, 4. ISC, 5. GPL-3.0-only, 6. Not open source]</dd>
</dl>

except above settings, for CI/CD, you'll also need configure gitub repsitory secrets
at page repo > settings > secrtes, and add the following secrets:

- PERSONAL_TOKEN (required for publishing document to git pages)
- TEST_PYPI_API_TOKEN (required for publishing dev release to testpypi)
- PYPI_API_TOKEN (required for publish )
