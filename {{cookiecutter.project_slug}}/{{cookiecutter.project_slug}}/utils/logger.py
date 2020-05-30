# -*- coding: utf-8 -*-

import sys
import logging


def init_logger(logfile, loglevel=logging.INFO):
    """
    Set the logging configuration for this application.
    The configuration string looks like this:
    ``[%(asctime)s] [%(levelname)s] [%(name)s] %(filename)s:%(lineno)d %(message)s``
    which results in a log entry such as:
    ``[03/18/2020 12:51:50PM] [INFO] main.py:185 Welcome! See main.py for examples``

    Returns
    -------
    logger: Logger
        An instance of ``Logger`` class.

    """
    log_str = "[%(asctime)s] [%(levelname)s] " \
              "[%(name)s] %(filename)s:%(lineno)d " \
              "%(message)s "

    datefmt='%m/%d/%Y %I:%M:%S%p'

    logger = logging.getLogger()
    logger.setLevel(loglevel)

    # set up some handlers
    console_handler = logging.StreamHandler(sys.stderr)
    # log the same to a file
    file_handler = logging.FileHandler(logfile, mode='w')

    formatter = logging.Formatter(fmt=log_str, datefmt=datefmt)
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
