# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest
import os
import os.path
from conflog import Conflog

class TestNoConf(unittest.TestCase):

    def setUp(self):
        os.unsetenv('CONFLOG_FORMAT')
        if 'CONFLOG_FORMAT' in os.environ:
            os.environ.pop('CONFLOG_FORMAT')
        self.logger_name = None
        self.conflog = None
        self.log_file = 'stage/test-integration/test-no-conf.log'

    # close handlers and remove log file on tearDown
    def tearDown(self):
        self.conflog.close_logger_handlers(self.logger_name)
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_get_logger_with_no_conf_file(self):
        self.logger_name = 'test_get_logger_with_no_conf_file'
        self.conflog = Conflog()
        logger = self.conflog.get_logger(self.logger_name)
        logger.debug('Some debug log message')
        logger.info('Some info log message')
        logger.warning('Some warning log message')
        logger.error('Some error log message')
        logger.critical('Some critical log message')
        # should not create any log file because file handler is not defined
        self.assertFalse(os.path.exists(self.log_file))
