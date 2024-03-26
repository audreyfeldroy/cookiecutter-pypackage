#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
{% if cookiecutter.use_numpy == 'y' -%}
    'numpy',{% endif %}
{% if cookiecutter.use_scipy == 'y' -%}
    'scipy',{% endif %}
{% if cookiecutter.use_matplotlib == 'y' -%}
    'matplotlib',{% endif %}
{% if cookiecutter.use_pyfar == 'y' -%}
    'pyfar',{% endif %}
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
    'bump2version',
    'wheel',
    'watchdog',
    'flake8',
    'coverage',
    'Sphinx',
    'twine',
    'pydata-sphinx-theme',
]

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
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
{%- if cookiecutter.open_source_license in license_classifiers %}
        '{{ license_classifiers[cookiecutter.open_source_license] }}',
{%- endif %}
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        {% for extension, details in cookiecutter._valid_versions|dictsort %}{% if extension == cookiecutter.minimum_python_version -%}{% for app in details.version_list -%}
        'Programming Language :: Python :: {{ app }}',
        {% endfor -%}{% endif %}{% endfor %}
    ],
    description="{{ cookiecutter.project_short_description }}",
    install_requires=requirements,
{%- if cookiecutter.open_source_license in license_classifiers %}
    license="{{ cookiecutter.open_source_license }}",
{%- endif %}
    long_description=readme,
    include_package_data=True,
    keywords='{{ cookiecutter.project_slug }}',
    name='{{ cookiecutter.project_slug }}',
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url="https://pyfar.org/",
    download_url="https://pypi.org/project/{{ cookiecutter.project_slug }}/",
    project_urls={
        "Bug Tracker": "https://github.com/{{ cookiecutter.git_username }}/{{ cookiecutter.project_slug }}/issues",
        "Documentation": "https://{{ cookiecutter.project_slug }}.readthedocs.io/",
        "Source Code": "https://github.com/{{ cookiecutter.git_username }}/{{ cookiecutter.project_slug }}",
    },
    version='{{ cookiecutter.version }}',
    zip_safe=False,
    python_requires='>={{ cookiecutter.minimum_python_version }}',
)
