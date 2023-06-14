# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest
import os
import os.path
from conflog import Conflog

class TestNoConf(unittest.TestCase):

    def setUp(self):
        os.unsetenv('CONFLOG_HANDLERS')
        if 'CONFLOG_HANDLERS' in os.environ:
            os.environ.pop('CONFLOG_HANDLERS')
        os.unsetenv('CONFLOG_DATEFMT')
        if 'CONFLOG_DATEFMT' in os.environ:
            os.environ.pop('CONFLOG_DATEFMT')
        os.unsetenv('CONFLOG_FORMAT')
        if 'CONFLOG_FORMAT' in os.environ:
            os.environ.pop('CONFLOG_FORMAT')
        os.unsetenv('CONFLOG_LEVEL')
        if 'CONFLOG_LEVEL' in os.environ:
            os.environ.pop('CONFLOG_LEVEL')
        os.unsetenv('CONFLOG_EXTRAS')
        if 'CONFLOG_EXTRAS' in os.environ:
            os.environ.pop('CONFLOG_EXTRAS')
        self.logger_name = None
        self.conflog = None
        self.log_file = 'stage/test-integration/test-no-conf.log'

    # close handlers and remove log file on tearDown
    def tearDown(self):
        self.conflog.close_logger_handlers(self.logger_name)
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_constructor_with_list_arg(self):
        self.logger_name = 'test_constructor_with_list_arg'
        self.conflog = Conflog(['tests-integration/fixtures/conflog.yaml'])
        logger = self.conflog.get_logger(self.logger_name)
        logger.debug('Some debug log message')
        logger.info('Some info log message')
        logger.warning('Some warning log message')
        logger.error('Some error log message')
        logger.critical('Some critical log message')
        # should not create any log file because file handler is not defined
        self.assertFalse(os.path.exists(self.log_file))

        # should have the config properties from config file
        config = self.conflog.get_config_properties()
        self.assertEqual(config['handlers'], 'stream,file')
        self.assertEqual(config['datefmt'], '%Y-%m-%d %H:%M:%S')
        self.assertEqual(config['filename'], 'stage/test-integration/test-yaml-conf.log')
        self.assertEqual(config['filemode'], 'w')
        self.assertEqual(config['format'],
                         '[YAML-CONFLOG] [%(env)s-%(id)s] %(levelname)s %(message)s')
        self.assertEqual(config['level'], 'info')
        self.assertEqual(config['extras']['env'], 'someenv')
        self.assertEqual(config['extras']['id'], 'someid')

    def test_constructor_with_string_arg(self):
        self.logger_name = 'test_constructor_with_string_arg'
        self.conflog = Conflog('tests-integration/fixtures/conflog.yaml')
        logger = self.conflog.get_logger(self.logger_name)
        logger.debug('Some debug log message')
        logger.info('Some info log message')
        logger.warning('Some warning log message')
        logger.error('Some error log message')
        logger.critical('Some critical log message')
        # should not create any log file because file handler is not defined
        self.assertFalse(os.path.exists(self.log_file))

        # should have the config properties from config file
        config = self.conflog.get_config_properties()
        self.assertEqual(config['handlers'], 'stream,file')
        self.assertEqual(config['datefmt'], '%Y-%m-%d %H:%M:%S')
        self.assertEqual(config['filename'], 'stage/test-integration/test-yaml-conf.log')
        self.assertEqual(config['filemode'], 'w')
        self.assertEqual(config['format'],
                         '[YAML-CONFLOG] [%(env)s-%(id)s] %(levelname)s %(message)s')
        self.assertEqual(config['level'], 'info')
        self.assertEqual(config['extras']['env'], 'someenv')
        self.assertEqual(config['extras']['id'], 'someid')

    def test_constructor_with_no_arg(self):
        self.logger_name = 'test_constructor_with_no_arg'
        self.conflog = Conflog()
        logger = self.conflog.get_logger(self.logger_name)
        logger.debug('Some debug log message')
        logger.info('Some info log message')
        logger.warning('Some warning log message')
        logger.error('Some error log message')
        logger.critical('Some critical log message')
        # should not create any log file because file handler is not defined
        self.assertFalse(os.path.exists(self.log_file))

        # should have no config properties
        config = self.conflog.get_config_properties()
        self.assertEqual(config, {})

    def test_constructor_with_string_arg_and_envvar_overwrites(self):

        # # set env var CONFLOG_FORMAT
        os.environ['CONFLOG_HANDLERS'] = 'file'
        os.environ['CONFLOG_DATEFMT'] = '%Y'
        os.environ['CONFLOG_FORMAT'] = '[ENVVAR-CONFLOG] [%(env)s-%(id)s] %(levelname)s %(message)s'
        os.environ['CONFLOG_LEVEL'] = 'critical'
        os.environ['CONFLOG_EXTRAS'] = 'env=overwriteenv,id=overwriteid'

        self.logger_name = 'test_constructor_with_string_arg'
        self.conflog = Conflog('tests-integration/fixtures/conflog.yaml')
        logger = self.conflog.get_logger(self.logger_name)
        logger.debug('Some debug log message')
        logger.info('Some info log message')
        logger.warning('Some warning log message')
        logger.error('Some error log message')
        logger.critical('Some critical log message')
        # should not create any log file because file handler is not defined
        self.assertFalse(os.path.exists(self.log_file))

        # should have the config properties from config file
        config = self.conflog.get_config_properties()
        self.assertEqual(config['handlers'], 'file')
        self.assertEqual(config['datefmt'], '%Y')
        self.assertEqual(config['filename'], 'stage/test-integration/test-yaml-conf.log')
        self.assertEqual(config['filemode'], 'w')
        self.assertEqual(config['format'],
                         '[ENVVAR-CONFLOG] [%(env)s-%(id)s] %(levelname)s %(message)s')
        self.assertEqual(config['level'], 'critical')
        self.assertEqual(config['extras'], 'env=overwriteenv,id=overwriteid')
