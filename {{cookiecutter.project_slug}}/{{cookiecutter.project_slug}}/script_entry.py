# -*- coding: utf-8 -*-
""" This is where we have the scripts that are going to be exposed as entry points in setup.py
"""
import logging

from business_logic import BusinessProcess  # pylint: disable=relative-import

log = logging.getLogger(__name__)
debug = log.isEnabledFor(logging.DEBUG)


def first_script():
    """ does something
    """
    # config, logConfig = pl_utils.initialize()

    business_process = BusinessProcess(1, 2)
    result = business_process.run()
