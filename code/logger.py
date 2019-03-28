# -*- coding: utf-8 -*-
import logging
LOG_FORMAT = '%(levelname)s | %(asctime)s | %(processName)s | %(message)s'
LOG_LEVEL = logging.DEBUG


class Logger(logging):
    def __init__(self, file_name):
        """
        constructor
        """
        self.basicConfig(format=LOG_FORMAT,
                         filename=file_name,
                         level=LOG_LEVEL)
