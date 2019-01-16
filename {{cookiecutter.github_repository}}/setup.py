#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    {%- if cookiecutter.command_line_interface|lower == 'click' %}
    'Click>=6.0',
    {%- endif %}
    # TODO: put package requirements here
]

setup_requirements = [
    'bumpversion>=0.5.3',
    'wheel>=0.29.0',
    'watchdog>=0.8.3',
    'Sphinx>=1.4.8',
    # TODO({{ cookiecutter.remote_username }}): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest>=2.9.2',
    'pytest-runner>=2.11.1',
    'flake8>=2.6.0',
    'tox>=2.3.1',
    'coverage>=4.1'
    # TODO: put package test requirements here
]

{%- set license_classifiers = {
    'MIT': 'License :: OSI Approved :: MIT License',
    'BSD-3-Clause': 'License :: OSI Approved :: BSD License',
    'ISC': 'License :: OSI Approved :: ISC License (ISCL)',
    'Apache-2.0': 'License :: OSI Approved :: Apache Software License',
    'GPL-3.0': 'License :: OSI Approved :: GPL-3.0 (GPLv3)'
} %}

setup(
    name='{{ cookiecutter.module_name }}',
    version='{{ cookiecutter.module_version }}',
    description="{{ cookiecutter.repository_summary }}",
    long_description=readme + '\n\n' + history,
    author="{{ cookiecutter.author_name.replace('\"', '\\\"') }}",
    author_email='{{ cookiecutter.author_email }}',
    url='https://github.com/{{ cookiecutter.remote_username }}/{{ cookiecutter.repository_slug }}',
    packages=find_packages(include=['{{ cookiecutter.module_name }}']),
    {%- if 'no' not in cookiecutter.command_line_interface|lower %}
    entry_points={
        'console_scripts': [
            '{{ cookiecutter.module_name }}={{ cookiecutter.module_name }}.cli:main'
        ]
    },
    {%- endif %}
    include_package_data=True,
    install_requires=requirements,
{%- if cookiecutter.copyright_license in license_classifiers %}
    license="{{ cookiecutter.copyright_license }}",
{%- endif %}
    zip_safe=False,
    keywords='{{ cookiecutter.module_name }}',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
{%- if cookiecutter.copyright_license in license_classifiers %}
        '{{ license_classifiers[cookiecutter.copyright_license] }}',
{%- endif %}
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
