import re
from setuptools import setup

init_py = open('{{cookiecutter.repo_name}}/__init__.py').read()
metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", init_py))

setup(
    name='{{cookiecutter.repo_name}}',
    version=metadata['version'],
    description=metadata['doc'],
    author=metadata['author'],
    author_email=metadata['email'],
    url=metadata['url'],
    packages=['{{cookiecutter.repo_name}}'],
    include_package_data=True,
    install_requires=[
    ],
    test_suite='nose.collector',
    license=open('LICENSE').read(),
)

