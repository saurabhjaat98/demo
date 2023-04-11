###############################################################################
# Copyright (c) 2021-present CorEdge - All Rights Reserved                    #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Manik Sidana <manik@coredge.io>, June 2021                       #
###############################################################################
import logging
import os
from logging import DEBUG
from logging.handlers import RotatingFileHandler

from ccp_server.util import ccp_context

# TODO: Fetch the project name from app during integration
PROJECT = 'CCP_MIDDLEWARE'

# log file will be stored inside the current .data folder, so the app can run in local without any setting
LOG_FILE_PATH = '/var/log/ccp.log'


class KGLogger:
    """
    Usage:
    LOG = KGLogger(__name__)
    LOG.debug('My debug string')
    """

    # TODO: Some of these parameters can be moved to a config file later
    # TODO: Change log path
    __LOG_FILE__ = os.environ.get("LOG_FILE_PATH", default=LOG_FILE_PATH)

    def __init__(self, name, level=DEBUG):
        """
        Method to initialise KGLogger
        :param name: Logger name
        :param level: Log level
        """
        audit_id = ccp_context.request_id()
        audit_id = audit_id if audit_id else ''
        self.format = f'%(asctime)s %(process)d {audit_id} %(levelname)s {PROJECT} ' \
                      f'%(filename)s:%(lineno)d %(message)s'
        self.name = name
        self.level = level
        self.logger = logging.getLogger(self.name)
        self.formatter = logging.Formatter(self.format)

        # Remove existing handlers from the logger to prevent duplicates
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)

        # Add a StreamHandler handler to send logs to the console
        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.console_handler)

        # Add a RotatingFileHandler to send logs to a file
        self.file_handler = RotatingFileHandler(
            self.__LOG_FILE__, maxBytes=5 * 1024 * 1024, backupCount=10
        )
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

        self.logger.setLevel(self.level)
        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warn = self.logger.warning
        self.error = self.logger.error
        self.critical = self.logger.critical


def configure_logger(level=DEBUG):
    """ Configure the logger so that logger can have the request ID"""
    LOG = KGLogger(name=__name__, level=level)
    return LOG


LOG = KGLogger(__name__)


def log(func):
    """
    Decorator to be added to a function which needs debug logging for entry/exit.
    Developer to ensure that it's not causing circular dependencies wherever used.
    """

    def inner(*args, **kwargs):
        if not callable(func):
            err = f"{func} is not callable."
            raise Exception(err)

        # Log a message indicating that the function is being entered with the request ID
        LOG.debug(
            f"Entering into {func.__module__}.{func.__qualname__}")

        # Call the original function and capture its result
        res = func(*args, **kwargs)

        # Log a message indicating that the function is being exited with the request ID
        LOG.debug(
            f"Exiting from {func.__module__}.{func.__qualname__}")

        return res

    return inner
