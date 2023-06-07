# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest
import os
import os.path
from logconf import Logconf

class TestMultiConf(unittest.TestCase):

    def setUp(self):
        os.unsetenv('LOGCONF_FORMAT')
        if 'LOGCONF_FORMAT' in os.environ:
            os.environ.pop('LOGCONF_FORMAT')
        self.logger_name = None
        self.logconf = None
        self.log_file = None

    # close handlers and remove log file on tearDown
    def tearDown(self):
        self.logconf.close_logger_handlers(self.logger_name)
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_get_logger_with_multi_conf_files(self):
        # should have yaml log file since yaml config is last in the conf_files
        self.log_file = 'stage/test-integration/test-yaml-conf.log'
        self.logger_name = 'test_get_logger_with_multi_conf_files'
        self.logconf = Logconf(conf_files=[
            'tests-integration/fixtures/logconf.ini',
            'tests-integration/fixtures/logconf.json',
            'tests-integration/fixtures/logconf.xml',
            'tests-integration/fixtures/logconf.yaml'
        ])
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
        # should have YAML-LOGCONF in the log message because yaml config is last in the conf_files
        self.assertEqual(content,
                            '[YAML-LOGCONF] [someenv-someid] INFO Some info log message\n'\
                            '[YAML-LOGCONF] [someenv-someid] WARNING Some warning log message\n'\
                            '[YAML-LOGCONF] [someenv-someid] ERROR Some error log message\n'\
                            '[YAML-LOGCONF] [someenv-someid] CRITICAL Some critical log message\n')

    def test_get_logger_with_multi_conf_files_reversed(self):
        # should have ini log file since ini config is last in the conf_files
        self.log_file = 'stage/test-integration/test-ini-conf.log'
        self.logger_name = 'test_get_logger_with_multi_conf_files'
        self.logconf = Logconf(conf_files=[
            'tests-integration/fixtures/logconf.yaml',
            'tests-integration/fixtures/logconf.xml',
            'tests-integration/fixtures/logconf.json',
            'tests-integration/fixtures/logconf.ini'
        ])
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
        # should have INI-LOGCONF in the log message because ini config is last in the conf_files
        self.assertEqual(content,
                            '[INI-LOGCONF] [someenv-someid] INFO Some info log message\n'\
                            '[INI-LOGCONF] [someenv-someid] WARNING Some warning log message\n'\
                            '[INI-LOGCONF] [someenv-someid] ERROR Some error log message\n'\
                            '[INI-LOGCONF] [someenv-someid] CRITICAL Some critical log message\n')

    def test_get_logger_with_multi_conf_files_envvar_override(self):
        # should have yaml log file since yaml config is last in the conf_files
        self.log_file = 'stage/test-integration/test-yaml-conf.log'
        self.logger_name = 'test_get_logger_with_multi_conf_files'
        os.environ['LOGCONF_FORMAT'] = '[ENVVAR-LOGCONF] [%(env)s-%(id)s] %(levelname)s %(message)s'
        self.logconf = Logconf(conf_files=[
            'tests-integration/fixtures/logconf.ini',
            'tests-integration/fixtures/logconf.json',
            'tests-integration/fixtures/logconf.xml',
            'tests-integration/fixtures/logconf.yaml'
        ])
        logger = self.logconf.get_logger(self.logger_name)
        os.unsetenv('LOGCONF_FORMAT')
        if 'LOGCONF_FORMAT' in os.environ:
            os.environ.pop('LOGCONF_FORMAT')
        logger.debug('Some debug log message')
        logger.info('Some info log message')
        logger.warning('Some warning log message')
        logger.error('Some error log message')
        logger.critical('Some critical log message')
        with open(self.log_file, 'r', encoding='utf-8') as stream:
            content = stream.read()
        # should exclude debug
        # should include info, warning, error, critical
        # should have ENVVAR-LOGCONF in the log message
        # because LOGCONF_FORMAT overrides all conf_files
        self.assertEqual(content,
                        '[ENVVAR-LOGCONF] [someenv-someid] INFO Some info log message\n'\
                        '[ENVVAR-LOGCONF] [someenv-someid] WARNING Some warning log message\n'\
                        '[ENVVAR-LOGCONF] [someenv-someid] ERROR Some error log message\n'\
                        '[ENVVAR-LOGCONF] [someenv-someid] CRITICAL Some critical log message\n')
