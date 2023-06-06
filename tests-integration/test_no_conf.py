# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code
import unittest
import os
import os.path
from logconf.logconf import Logconf

class TestNoConf(unittest.TestCase):

    def setUp(self):
        self.logger_name = None
        self.logconf = None
        self.log_file = 'stage/test-integration/test-no-conf.log'

    # close handlers and remove log file on tearDown
    def tearDown(self):
        self.logconf.close_logger_handlers(self.logger_name)
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_get_logger_with_no_conf_file(self):
        self.logger_name = 'test_get_logger_with_no_conf_file'
        self.logconf = Logconf()
        logger = self.logconf.get_logger(self.logger_name)
        logger.debug('Some debug log message')
        logger.info('Some info log message')
        logger.warning('Some warning log message')
        logger.error('Some error log message')
        logger.critical('Some critical log message')
        # should not create any log file because file handler is not defined
        self.assertFalse(os.path.exists(self.log_file))
