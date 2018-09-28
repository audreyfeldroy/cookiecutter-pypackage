# -*- coding: utf-8 -*-
""" Application configuration. """

import os

from typing import List, Union

from decouple import config


class Config(object):
    """Config

    The configuration for the application. Each configuration option is specified as a class
    constant with a value derived from the environment using the :meth:`decouple.config` function.

    Default values, when specified, should be production-safe. If a production-safe value is
    dependent on usage, a default is not specified and is instead expected to be configured by
    the environment.
    """

    ##
    #: The `APP_DIR` points to the location of the Flask app on the local
    #: filesystem.
    #:
    #: This value is not configurable as it derives itself from the path of this
    #: settings file, as it is assumed to be in the `APP_DIR`.
    #:
    APP_DIR: str = os.path.abspath(os.path.dirname(__file__))

    ##
    #: The `PROJECT_ROOT` specifies the path to the project (the directory
    #: containing migrations, tests, configurations, etc).
    #:
    #: This value is not configurable as it derives itself from the parent
    #: directory of the `APP_DIR`.
    #:
    PROJECT_ROOT: str = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    ##
    #: The `ENV` specifies the environment context that the application is
    #: being run in (local, development, staging, production).
    #:
    #: In general it is considered bad practice to write code that depends on
    #: this value: the application should be unaware of its environment context.
    #:
    #: However, this value may be used to restrict or prevent certain actions
    #: based on context. For example, disabling dangerous or destructive
    #: administrative actions in a production environment.
    #:
    #: Default: `production`
    #:
    ENV: str = config('ENV', 'production')

    ##
    #: The `DEBUG` flag is a standard universal flag for increasing verbosity
    #: and enabling developer features.
    #:
    #: Default: `False`
    #:
    DEBUG: bool = config('DEBUG', False, cast=bool)

    ##
    #: The `LOG_LEVEL` is used to configure logging verbosity.
    #:
    #: Possible values are:
    #:
    #:   - `NOTSET`
    #:   - `DEBUG`
    #:   - `INFO`
    #:   - `WARNING`
    #:   - `ERROR`
    #:   - `CRITICAL`
    #:
    #: Default: `INFO` (or `DEBUG` if the `DEBUG` flag is set)
    #:
    LOG_LEVEL: str = config('LOG_LEVEL', ('DEBUG' if DEBUG else 'INFO')).upper()

    ##
    #: The `LOG_PRETTY` flag is used to make log messaging more human-readable.
    #:
    #: Most often used in development contexts.
    #:
    #: Default: `False`
    #:
    LOG_PRETTY: bool = config('LOG_PRETTY', False, cast=bool)
