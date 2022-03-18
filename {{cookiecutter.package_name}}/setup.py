#!/usr/bin/env python

"""The setup script."""
from os import path
from setuptools import setup, find_packages
import sys
import versioneer

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(path.join(here, 'requirements.txt')) as requirements_file:
    # Parse requirements.txt, ignoring any commented-out lines.
    requirements = [line for line in requirements_file.read().splitlines()
                    if not line.startswith('#')]

{%- set license_classifiers = {
    'MIT license': 'License :: OSI Approved :: MIT License',
    'BSD license': 'License :: OSI Approved :: BSD License',
    'ISC license': 'License :: OSI Approved :: ISC License (ISCL)',
    'Apache Software License 2.0': 'License :: OSI Approved :: Apache Software License',
    'GNU General Public License v3': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
} %}

setup(
    author="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
    author_email='{{ cookiecutter.email }}',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    description="{{ cookiecutter.project_short_description }}",
    entry_points={
        'console_scripts': [
            #'{{ cookiecutter.package_name }}={{ cookiecutter.package_name }}:some_function',
        ],
    },
    install_requires=requirements,
{%- if cookiecutter.open_source_license in license_classifiers %}
    license="{{ cookiecutter.open_source_license }}",
{%- endif %}
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='{{ cookiecutter.package_name }}',
    name='{{ cookiecutter.package_name }}',
    packages=find_packages(include=['{{ cookiecutter.package_name }}', '{{ cookiecutter.package_name }}.*']),
    test_suite='tests',
    url='https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    zip_safe=False,
    extras_require={
        'tests': ['pytest', 'codecov', 'pytest-cov'],
        'docs': ['sphinx', 'sphinx-rtd-theme', 'myst-parser', 'myst-nb', 'sphinx-panels', 'autodocs']
    }
)
