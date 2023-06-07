# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest
import os
import os.path
from logconf import Logconf

class TestYamlConf(unittest.TestCase):

    def setUp(self):
        os.unsetenv('LOGCONF_FORMAT')
        if 'LOGCONF_FORMAT' in os.environ:
            os.environ.pop('LOGCONF_FORMAT')
        self.logger_name = None
        self.logconf = None
        self.log_file = 'stage/test-integration/test-yaml-conf.log'

    # close handlers and remove log file on tearDown
    def tearDown(self):
        self.logconf.close_logger_handlers(self.logger_name)
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_get_logger_with_single_conf_file(self):
        self.logger_name = 'test_get_logger_with_single_conf_file'
        self.logconf = Logconf(conf_files=['tests-integration/fixtures/logconf.yaml'])
        logger = self.logconf.get_logger(self.logger_name)
        logger.debug('Some debug log message')
        logger.info('Some info log message')
        logger.warning('Some warning log message')
        logger.error('Some error log message')
        logger.critical('Some critical log message')
        with open(self.log_file, 'r', encoding='utf-8') as stream:
            content = stream.read()
        # should exclude debug
        # should include info, warning, error, critical
        self.assertEqual(content,
                            '[YAML-LOGCONF] [someenv-someid] INFO Some info log message\n'\
                            '[YAML-LOGCONF] [someenv-someid] WARNING Some warning log message\n'\
                            '[YAML-LOGCONF] [someenv-someid] ERROR Some error log message\n'\
                            '[YAML-LOGCONF] [someenv-someid] CRITICAL Some critical log message\n')

    def test_get_logger_with_single_conf_file_with_excluded_level(self):
        self.logger_name = 'test_get_logger_with_single_conf_file_with_excluded_level'
        self.logconf = Logconf(conf_files=['tests-integration/fixtures/logconf.yaml'])
        logger = self.logconf.get_logger(self.logger_name)
        logger.debug('Some debug log message')
        with open(self.log_file, 'r', encoding='utf-8') as stream:
            content = stream.read()
        # should have empty log message because debug level is excluded
        self.assertEqual(content, '')

    def test_get_logger_with_single_conf_file_with_stream_handler_only(self):
        self.logger_name = 'test_get_logger_with_single_conf_file_stream_only'
        self.logconf = Logconf(conf_files=['tests-integration/fixtures/logconf-stream-only.yaml'])
        logger = self.logconf.get_logger(self.logger_name)
        logger.info('Some info log message')
        # should not create any log file because file handler is not defined
        self.assertFalse(os.path.exists(self.log_file))

    def test_get_logger_with_single_conf_file_with_empty_config(self):
        self.logger_name = 'test_get_logger_with_single_conf_file_with_empty_config'
        self.logconf = Logconf(conf_files=['tests-integration/fixtures/logconf-empty.yaml'])
        logger = self.logconf.get_logger(self.logger_name)
        logger.info('Some info log message')
        # should not create any log file because
        # file handler is not defined in default handlers config
        self.assertFalse(os.path.exists(self.log_file))
