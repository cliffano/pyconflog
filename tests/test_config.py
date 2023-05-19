from logconf.config import Config
import logging
import unittest
from unittest.mock import patch

CUSTOM_CONF = {
    'datefmt': '%y%m%d',
    'filename': 'somelogconf.log',
    'filemode': 'rw',
    'format': 'somelog %(asctime)s --> %(name)s - %(levelname)s - %(message)s',
    'level': 'critical'
}

OVERWRITE_CONF = {
    'datefmt': '%d%m%y',
    'filename': 'overwritelogconf.log',
    'filemode': 'r',
    'format': 'overwritelog %(asctime)s --> %(name)s - %(levelname)s - %(message)s',
    'level': 'debug'
}

class TestConfig(unittest.TestCase):

    def test_get_defaults(self):
        config = Config()
        self.assertEqual(config.get_datefmt(), '%d-%b-%y %H:%M:%S')
        self.assertEqual(config.get_filename(), 'logconf.log')
        self.assertEqual(config.get_filemode(), 'w')
        self.assertEqual(config.get_format(), '%(asctime)s --> %(name)s - %(levelname)s - %(message)s')
        self.assertEqual(config.get_level(), logging.INFO)

    @patch('logconf.loaders.ini_loader.load')
    def test_get_config_from_ini(self, func):
        func.return_value = CUSTOM_CONF
        config = Config(conf_files=['somefile.ini'])
        self.assertEqual(config.get_datefmt(), '%y%m%d')
        self.assertEqual(config.get_filename(), 'somelogconf.log')
        self.assertEqual(config.get_filemode(), 'rw')
        self.assertEqual(config.get_format(), 'somelog %(asctime)s --> %(name)s - %(levelname)s - %(message)s')
        self.assertEqual(config.get_level(), logging.CRITICAL)

    @patch('logconf.loaders.json_loader.load')
    def test_get_config_from_json(self, func):
        func.return_value = CUSTOM_CONF
        config = Config(conf_files=['somefile.json'])
        self.assertEqual(config.get_datefmt(), '%y%m%d')
        self.assertEqual(config.get_filename(), 'somelogconf.log')
        self.assertEqual(config.get_filemode(), 'rw')
        self.assertEqual(config.get_format(), 'somelog %(asctime)s --> %(name)s - %(levelname)s - %(message)s')
        self.assertEqual(config.get_level(), logging.CRITICAL)

    @patch('logconf.loaders.xml_loader.load')
    def test_get_config_from_xml(self, func):
        func.return_value = CUSTOM_CONF
        config = Config(conf_files=['somefile.xml'])
        self.assertEqual(config.get_datefmt(), '%y%m%d')
        self.assertEqual(config.get_filename(), 'somelogconf.log')
        self.assertEqual(config.get_filemode(), 'rw')
        self.assertEqual(config.get_format(), 'somelog %(asctime)s --> %(name)s - %(levelname)s - %(message)s')
        self.assertEqual(config.get_level(), logging.CRITICAL)
    
    @patch('logconf.loaders.yaml_loader.load')
    def test_get_config_from_yaml(self, func):
        func.return_value = CUSTOM_CONF
        config = Config(conf_files=['somefile.yaml'])
        self.assertEqual(config.get_datefmt(), '%y%m%d')
        self.assertEqual(config.get_filename(), 'somelogconf.log')
        self.assertEqual(config.get_filemode(), 'rw')
        self.assertEqual(config.get_format(), 'somelog %(asctime)s --> %(name)s - %(levelname)s - %(message)s')
        self.assertEqual(config.get_level(), logging.CRITICAL)

    @patch('logconf.loaders.environ_loader.load')
    def test_get_config_from_environ(self, func):
        func.return_value = CUSTOM_CONF
        config = Config()
        self.assertEqual(config.get_datefmt(), '%y%m%d')
        self.assertEqual(config.get_filename(), 'somelogconf.log')
        self.assertEqual(config.get_filemode(), 'rw')
        self.assertEqual(config.get_format(), 'somelog %(asctime)s --> %(name)s - %(levelname)s - %(message)s')
        self.assertEqual(config.get_level(), logging.CRITICAL)

    @patch('logconf.loaders.ini_loader.load')
    @patch('logconf.loaders.environ_loader.load')
    def test_get_config_with_ini_overwritten_by_environ(self, func_ini, func_environ):
        func_ini.return_value = CUSTOM_CONF
        func_environ.return_value = OVERWRITE_CONF
        config = Config(conf_files=['somefile.ini'])
        self.assertEqual(config.get_datefmt(), '%d%m%y')
        self.assertEqual(config.get_filename(), 'overwritelogconf.log')
        self.assertEqual(config.get_filemode(), 'r')
        self.assertEqual(config.get_format(), 'overwritelog %(asctime)s --> %(name)s - %(levelname)s - %(message)s')
        self.assertEqual(config.get_level(), logging.DEBUG)

    @patch('logconf.loaders.ini_loader.load')
    @patch('logconf.loaders.yaml_loader.load')
    def test_get_config_with_ini_overwritten_by_yaml(self, func_ini, func_yaml):
        func_ini.return_value = CUSTOM_CONF
        func_yaml.return_value = OVERWRITE_CONF
        config = Config(conf_files=['somefile.ini', 'somefile.yaml'])
        self.assertEqual(config.get_datefmt(), '%d%m%y')
        self.assertEqual(config.get_filename(), 'overwritelogconf.log')
        self.assertEqual(config.get_filemode(), 'r')
        self.assertEqual(config.get_format(), 'overwritelog %(asctime)s --> %(name)s - %(levelname)s - %(message)s')
        self.assertEqual(config.get_level(), logging.DEBUG)

    @patch('logconf.loaders.yaml_loader.load')
    @patch('logconf.loaders.ini_loader.load')
    def test_get_config_with_yaml_overwritten_by_ini(self, func_yaml, func_ini):
        func_yaml.return_value = CUSTOM_CONF
        func_ini.return_value = OVERWRITE_CONF
        config = Config(conf_files=['somefile.yaml', 'somefile.ini'])
        self.assertEqual(config.get_datefmt(), '%d%m%y')
        self.assertEqual(config.get_filename(), 'overwritelogconf.log')
        self.assertEqual(config.get_filemode(), 'r')
        self.assertEqual(config.get_format(), 'overwritelog %(asctime)s --> %(name)s - %(levelname)s - %(message)s')
        self.assertEqual(config.get_level(), logging.DEBUG)

if __name__ == '__main__':
    unittest.main()