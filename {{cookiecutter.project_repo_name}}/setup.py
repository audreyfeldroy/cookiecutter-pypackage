#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

about = {}
with open(os.path.join(here, '{{ cookiecutter.project_slug }}', '__version__.py'), 'r') as f:
    exec(f.read(), about)

reqs = [line.strip() for line in open('requirements.txt')]

{%- set license_classifiers = {
    'Apache Software License 2.0': 'License :: OSI Approved :: Apache Software License',
    'MIT license': 'License :: OSI Approved :: MIT License',
    'BSD license': 'License :: OSI Approved :: BSD License',
    'ISC license': 'License :: OSI Approved :: ISC License (ISCL)',
    'GNU General Public License v3': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
} %}

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Natural Language :: English',
    "Programming Language :: Python :: 2",
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Topic :: Scientific/Engineering :: Atmospheric Science',
{%- if cookiecutter.open_source_license in license_classifiers %}
    '{{ license_classifiers[cookiecutter.open_source_license] }}',
{%- endif %}
]

setup(name='{{ cookiecutter.project_slug }}',
      version=about['__version__'],
      description="{{ cookiecutter.project_short_description }}",
      long_description=README + '\n\n' + CHANGES,
      author=about['__author__'],
      author_email=about['__email__'],
      url='https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_repo_name }}',
      classifiers=classifiers,
{%- if cookiecutter.open_source_license in license_classifiers %}
      license="{{ cookiecutter.open_source_license }}",
{%- endif %}
      keywords='wps pywps birdhouse {{ cookiecutter.project_slug }}',
      packages=find_packages(),
      include_package_data=True,
      install_requires=reqs,
      entry_points={
          'console_scripts': [
             '{{ cookiecutter.project_slug }}={{ cookiecutter.project_slug }}.cli:cli',
          ]},)
