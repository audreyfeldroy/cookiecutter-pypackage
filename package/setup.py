#!/usr/bin/env python

import os
import sys

import {{ project.repo_name }}

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst', 'rt').read()
history = open('HISTORY.rst', 'rt').read()

setup(
    name='{{ project.repo_name }}',
    version={{ project.repo_name }}.__version__,
    description='{{ project.project_short_description }}',
    long_description=readme + '\n\n' + history,
    author='{{ project.full_name }}',
    author_email='{{ project.email }}',
    url='https://github.com/{{ project.github_username }}/{{ project.repo_name }}',
    packages=[
        '{{ project.repo_name }}',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='{{ project.repo_name }}',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
