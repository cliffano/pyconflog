# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from unittest.mock import patch
import unittest
import logging
from conflog.config import Config

CUSTOM_CONF = {
    'handlers': 'file',
    'datefmt': '%y%m%d',
    'filename': 'someconflog.log',
    'filemode': 'rw',
    'format': 'somelog %(asctime)s --> %(name)s - %(levelname)s - %(message)s',
    'level': 'critical',
    'extras': 'some_extra1=some_value1,some_extra2=some_value2'
}

OVERWRITE_CONF = {
    'handlers': 'stream,file',
    'datefmt': '%d%m%y',
    'filename': 'overwriteconflog.log',
    'filemode': 'r',
    'format': 'overwritelog %(asctime)s --> %(name)s - %(levelname)s - %(message)s',
    'level': 'debug',
    'extras': 'some_overwrite_extra1=some_overwrite_value1'
}

class TestConfig(unittest.TestCase):

    def test_get_defaults(self):
        config = Config()
        self.assertEqual(config.get_handlers(), ['stream'])
        self.assertEqual(config.get_datefmt(), '%d-%b-%y %H:%M:%S')
        self.assertEqual(config.get_filename(), 'conflog.log')
        self.assertEqual(config.get_filemode(), 'w')
        self.assertEqual(config.get_format(),
                         '%(asctime)s --> %(name)s - %(levelname)s - %(message)s')
        self.assertEqual(config.get_level(), logging.INFO)
        self.assertEqual(config.get_extras(), {})

    @patch('conflog.loaders.ini_loader.load')
    def test_get_config_from_ini(self, func): # pylint: disable=unused-argument
        func.return_value = CUSTOM_CONF
        config = Config(conf_files=['somefile.ini'])
        self.assertEqual(config.get_handlers(), ['file'])
        self.assertEqual(config.get_datefmt(), '%y%m%d')
        self.assertEqual(config.get_filename(), 'someconflog.log')
        self.assertEqual(config.get_filemode(), 'rw')
        self.assertEqual(config.get_format(),
                         'somelog %(asctime)s --> %(name)s - %(levelname)s - %(message)s')
        self.assertEqual(config.get_level(), logging.CRITICAL)
        extras = config.get_extras()
        self.assertEqual(len(extras.keys()), 2)
        self.assertEqual(extras['some_extra1'], 'some_value1')
        self.assertEqual(extras['some_extra2'], 'some_value2')

    @patch('conflog.loaders.json_loader.load')
    def test_get_config_from_json(self, func): # pylint: disable=unused-argument
        func.return_value = CUSTOM_CONF
        config = Config(conf_files=['somefile.json'])
        self.assertEqual(config.get_handlers(), ['file'])
        self.assertEqual(config.get_datefmt(), '%y%m%d')
        self.assertEqual(config.get_filename(), 'someconflog.log')
        self.assertEqual(config.get_filemode(), 'rw')
        self.assertEqual(config.get_format(),
                         'somelog %(asctime)s --> %(name)s - %(levelname)s - %(message)s')
        self.assertEqual(config.get_level(), logging.CRITICAL)
        extras = config.get_extras()
        self.assertEqual(len(extras.keys()), 2)
        self.assertEqual(extras['some_extra1'], 'some_value1')
        self.assertEqual(extras['some_extra2'], 'some_value2')

    @patch('conflog.loaders.xml_loader.load')
    def test_get_config_from_xml(self, func): # pylint: disable=unused-argument
        func.return_value = CUSTOM_CONF
        config = Config(conf_files=['somefile.xml'])
        self.assertEqual(config.get_handlers(), ['file'])
        self.assertEqual(config.get_datefmt(), '%y%m%d')
        self.assertEqual(config.get_filename(), 'someconflog.log')
        self.assertEqual(config.get_filemode(), 'rw')
        self.assertEqual(config.get_format(),
                         'somelog %(asctime)s --> %(name)s - %(levelname)s - %(message)s')
        self.assertEqual(config.get_level(), logging.CRITICAL)
        extras = config.get_extras()
        self.assertEqual(len(extras.keys()), 2)
        self.assertEqual(extras['some_extra1'], 'some_value1')
        self.assertEqual(extras['some_extra2'], 'some_value2')

    @patch('conflog.loaders.yaml_loader.load')
    def test_get_config_from_yaml(self, func): # pylint: disable=unused-argument
        func.return_value = CUSTOM_CONF
        config = Config(conf_files=['somefile.yaml'])
        self.assertEqual(config.get_handlers(), ['file'])
        self.assertEqual(config.get_datefmt(), '%y%m%d')
        self.assertEqual(config.get_filename(), 'someconflog.log')
        self.assertEqual(config.get_filemode(), 'rw')
        self.assertEqual(config.get_format(),
                         'somelog %(asctime)s --> %(name)s - %(levelname)s - %(message)s')
        self.assertEqual(config.get_level(), logging.CRITICAL)
        extras = config.get_extras()
        self.assertEqual(len(extras.keys()), 2)
        self.assertEqual(extras['some_extra1'], 'some_value1')
        self.assertEqual(extras['some_extra2'], 'some_value2')

    @patch('conflog.loaders.environ_loader.load')
    def test_get_config_from_environ(self, func): # pylint: disable=unused-argument
        func.return_value = CUSTOM_CONF
        config = Config()
        self.assertEqual(config.get_handlers(), ['file'])
        self.assertEqual(config.get_datefmt(), '%y%m%d')
        self.assertEqual(config.get_filename(), 'someconflog.log')
        self.assertEqual(config.get_filemode(), 'rw')
        self.assertEqual(config.get_format(),
                         'somelog %(asctime)s --> %(name)s - %(levelname)s - %(message)s')
        self.assertEqual(config.get_level(), logging.CRITICAL)
        extras = config.get_extras()
        self.assertEqual(len(extras.keys()), 2)
        self.assertEqual(extras['some_extra1'], 'some_value1')
        self.assertEqual(extras['some_extra2'], 'some_value2')

    @patch('conflog.loaders.yaml_loader.load')
    @patch('conflog.loaders.ini_loader.load')
    def test_get_config_with_ini_overwritten_by_yaml_sequence(self, func_ini, func_yaml):
        func_ini.return_value = CUSTOM_CONF
        func_yaml.return_value = OVERWRITE_CONF
        config = Config(conf_files=['somefile.ini', 'somefile.yaml'])
        self.assertEqual(config.get_handlers(), ['stream', 'file'])
        self.assertEqual(config.get_datefmt(), '%d%m%y')
        self.assertEqual(config.get_filename(), 'overwriteconflog.log')
        self.assertEqual(config.get_filemode(), 'r')
        self.assertEqual(config.get_format(),
                         'overwritelog %(asctime)s --> %(name)s - %(levelname)s - %(message)s')
        self.assertEqual(config.get_level(), logging.DEBUG)
        extras = config.get_extras()
        self.assertEqual(len(extras.keys()), 1)
        self.assertEqual(extras['some_overwrite_extra1'], 'some_overwrite_value1')

    @patch('conflog.loaders.ini_loader.load')
    @patch('conflog.loaders.yaml_loader.load')
    def test_get_config_with_yaml_overwritten_by_ini_sequence(self, func_yaml, func_ini):
        func_yaml.return_value = CUSTOM_CONF
        func_ini.return_value = OVERWRITE_CONF
        config = Config(conf_files=['somefile.yaml', 'somefile.ini'])
        self.assertEqual(config.get_handlers(), ['stream', 'file'])
        self.assertEqual(config.get_datefmt(), '%d%m%y')
        self.assertEqual(config.get_filename(), 'overwriteconflog.log')
        self.assertEqual(config.get_filemode(), 'r')
        self.assertEqual(config.get_format(),
                         'overwritelog %(asctime)s --> %(name)s - %(levelname)s - %(message)s')
        self.assertEqual(config.get_level(), logging.DEBUG)
        extras = config.get_extras()
        self.assertEqual(len(extras.keys()), 1)
        self.assertEqual(extras['some_overwrite_extra1'], 'some_overwrite_value1')

    @patch('conflog.loaders.environ_loader.load')
    @patch('conflog.loaders.ini_loader.load')
    def test_get_config_with_ini_overwritten_by_environ(self, func_ini, func_environ):
        func_ini.return_value = CUSTOM_CONF
        func_environ.return_value = OVERWRITE_CONF
        config = Config(conf_files=['somefile.ini'])
        self.assertEqual(config.get_handlers(), ['stream', 'file'])
        self.assertEqual(config.get_datefmt(), '%d%m%y')
        self.assertEqual(config.get_filename(), 'overwriteconflog.log')
        self.assertEqual(config.get_filemode(), 'r')
        self.assertEqual(config.get_format(),
                         'overwritelog %(asctime)s --> %(name)s - %(levelname)s - %(message)s')
        self.assertEqual(config.get_level(), logging.DEBUG)
        extras = config.get_extras()
        self.assertEqual(len(extras.keys()), 1)
        self.assertEqual(extras['some_overwrite_extra1'], 'some_overwrite_value1')

    @patch('conflog.loaders.environ_loader.load')
    @patch('conflog.loaders.ini_loader.load')
    def test_get_config_with_ini_overwritten_by_conf_dict(self, func_ini, func_environ):
        func_ini.return_value = CUSTOM_CONF
        func_environ.return_value = OVERWRITE_CONF
        conf_dict = {
            'handlers': 'stream',
            'datefmt': '%y',
            'filename': 'overwriteconfdictlog.log',
            'filemode': 'w',
            'format': '%(message)s',
            'level': 'critical'
        }
        config = Config(conf_files=['somefile.ini'], conf_dict=conf_dict)
        self.assertEqual(config.get_handlers(), ['stream'])
        self.assertEqual(config.get_datefmt(), '%y')
        self.assertEqual(config.get_filename(), 'overwriteconfdictlog.log')
        self.assertEqual(config.get_filemode(), 'w')
        self.assertEqual(config.get_format(), '%(message)s')
        self.assertEqual(config.get_level(), logging.CRITICAL)
