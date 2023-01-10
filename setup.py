# !/usr/bin/env python

from distutils.core import setup
setup(
    name='cookiecutter-netbox-plugin',
    packages=[],
    version='0.1.0',
    description='Cookiecutter template for a NetBox plugin',
    author='Arthur Hanson',
    license='BSD',
    author_email='ahanson@netboxlabs.com',
    url='https://github.com/netbox-community/cookiecutter-netbox-plugin',
    keywords=['cookiecutter', 'template', 'package', 'netbox'],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
    ],
)
