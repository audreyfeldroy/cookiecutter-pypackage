# -*- coding: utf-8 -*-
"""Commandline utils"""
import logging


def countToLogLevel(count: int) -> int:
    """Map the occurence of the command line option verbose to the log level"""
    if count == 0:
        return logging.ERROR
    elif count == 1:
        return logging.WARNING
    elif count == 2:
        return logging.INFO
    else:
        return logging.DEBUG
