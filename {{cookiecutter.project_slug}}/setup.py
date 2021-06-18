#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The setup script."""

from decimal import Decimal
import os
import os.path
from typing import List

# This must be above distutils, despite flake8's opinions.  Otherwise,
# this diagnostic is emitted:

# UserWarning: Distutils was imported before Setuptools. This usage is
# discouraged and may exhibit undesirable behaviors or errors. Please
# use Setuptools' objects directly or at least import Setuptools
# first.
from setuptools import find_packages, setup


from distutils.cmd import Command  # noqa: I100


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements: List[str] = []

test_requirements: List[str] = ['pytest>=3']

{%- set license_classifiers = {
    'MIT license': 'License :: OSI Approved :: MIT License',
    'BSD license': 'License :: OSI Approved :: BSD License',
    'ISC license': 'License :: OSI Approved :: ISC License (ISCL)',
    'Apache Software License 2.0': 'License :: OSI Approved :: Apache Software License',
    'GNU General Public License v3': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
} %}


# From https://github.com/bluelabsio/records-mover/blob/master/setup.py
class CoverageRatchetCommand(Command):
    description = 'Run coverage ratchet'
    user_options = []  # type: ignore
    coverage_file: str
    coverage_source_file: str
    coverage_url: str
    type_of_coverage: str

    def finalize_options(self) -> None:
        pass

    def run(self) -> None:
        """Run command."""
        import xml.etree.ElementTree as ET

        tree = ET.parse(self.coverage_source_file)
        new_coverage = Decimal(tree.getroot().attrib["line-rate"]) * 100

        if not os.path.exists(self.coverage_file):
            with open(self.coverage_file, 'w') as f:
                f.write('0')

        with open(self.coverage_file, 'r') as f:
            high_water_mark = Decimal(f.read())

        if new_coverage < high_water_mark:
            raise Exception(
                f"{self.type_of_coverage} coverage used to be {high_water_mark}; "
                f"down to {new_coverage}%.  Fix by viewing '{self.coverage_url}'")
        elif new_coverage > high_water_mark:
            with open(self.coverage_file, 'w') as f:
                f.write(str(new_coverage))
            print(f"Just ratcheted coverage up to {new_coverage}%")
        else:
            print(f"Code coverage steady at {new_coverage}%")


class TestCoverageRatchetCommand(CoverageRatchetCommand):
    def initialize_options(self) -> None:
        """Set default values for options."""
        self.type_of_coverage = 'Test'
        self.coverage_url = 'cover/index.html'
        self.coverage_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'metrics',
            'coverage_high_water_mark'
        )
        self.coverage_source_file = "coverage.xml"


class MypyCoverageRatchetCommand(CoverageRatchetCommand):
    def initialize_options(self) -> None:
        """Set default values for options."""
        self.type_of_coverage = 'Mypy'
        self.coverage_url = 'typecover/index.html'
        self.coverage_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'metrics',
            'mypy_high_water_mark'
        )
        self.coverage_source_file = "typecover/cobertura.xml"


setup(
    author="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
    author_email='{{ cookiecutter.email }}',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
{%- if cookiecutter.open_source_license in license_classifiers %}
        '{{ license_classifiers[cookiecutter.open_source_license] }}',
{%- endif %}
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="{{ cookiecutter.project_short_description.replace('\"', '\\\"') }}",  # noqa: E501
    {%- if 'no' not in cookiecutter.command_line_interface|lower %}
    entry_points={
        'console_scripts': [
            '{{ cookiecutter.project_slug }}={{ cookiecutter.project_slug }}.cli:main',
        ],
    },
    {%- endif %}
    cmdclass={
        'coverage_ratchet': TestCoverageRatchetCommand,
        'mypy_ratchet': MypyCoverageRatchetCommand,
    },
    install_requires=requirements,
{%- if cookiecutter.open_source_license in license_classifiers %}
    license="{{ cookiecutter.open_source_license }}",
{%- endif %}
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='{{ cookiecutter.project_slug }}',
    name='{{ cookiecutter.project_slug }}',
    packages=find_packages(include=['{{ cookiecutter.project_slug }}',
                                    '{{ cookiecutter.project_slug }}.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}',
    version='{{ cookiecutter.version }}',
    zip_safe=False,
)
