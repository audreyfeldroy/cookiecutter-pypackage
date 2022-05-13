"""
Logs
====
``loguru.logger`` setup for console and file logging.
"""

import pathlib
import loguru
import sys
from datetime import datetime
from os import getlogin
from {{ cookiecutter.project_slug }}.__init__ import __version__, __appname__


def get_loguru(
    app_name,
    version,
    file_logs_folder,
):
    """Function to setup a ``loguru.logger`` for console and file-log as well.
    Copy this function into any project for quick setup.

    Parameters
    ----------
    app_name : str
        Name of your app. Will be in ``extra``
    version : str
        Version of your app. Will be in ``extra``
    file_logs_folder : path
        Path to save your file txt logs.
    Returns
    -------
    loguru.logger
    Examples
    --------
    >>> from vmo_exporter.log import logger
    >>> logger.info('This log is written on console and in file as well!')
    """

    logger = loguru.logger
    logs_dir_server = pathlib.Path(file_logs_folder)
    log_name = f"LOG_{app_name}_{version}__{datetime.utcnow().strftime('%Y-%m-%d')}.log"
    LOG_PATH = logs_dir_server.joinpath(log_name)
    LOG_PATH_ALT = pathlib.Path.home().joinpath('Desktop').joinpath(log_name)

    user = getlogin()
    default_fmt = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    console_fmt = "<cyan>{name: <35}</cyan>:<cyan>{function: <28}</cyan>:<cyan>{line: <3}</cyan> | <level>{level: <8}</level> | <level>{message}</level>"
    file_fmt = "[{elapsed}] [{time}] [{extra[app]}] [{extra[version]}] [{extra[user]}] [{level: <7}] [{thread.name: <30}] - {name: <35}:{function: <32}:{line: >3} - {message}"

    def patching(record):
        record['extra']['user'] = getlogin()
        record['extra']['app'] = app_name
        record['extra']['version'] = version

    logger.remove()
    logger.add(sys.stderr, level='TRACE', format=console_fmt)  # TODO: Set to DEBUG or INFO in production
    logger = logger.opt(colors=True)
    if not pathlib.Path(file_logs_folder).exists():
        LOG_PATH = LOG_PATH_ALT

    logger.add(LOG_PATH, level='TRACE', format=file_fmt)

    logger = logger.patch(patching)
    print(f'Logging into: {LOG_PATH}')

    return logger


logger = get_loguru(
    app_name=__appname__,
    version=__version__,
    file_logs_folder=r'\\MSTM1BDB33\Apps\__LOGS'\
)
