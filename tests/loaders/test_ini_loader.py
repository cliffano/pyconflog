# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
from unittest.mock import patch, mock_open
import unittest.mock
import unittest
import configparser
from logconf.loaders.ini_loader import load

INI_WITH_PARAMS = '''[logconf]
datefmt: %%Y
filename: somelogconf.log
filemode: w
format: Some Log %%(asctime)s
level: critical
'''

INI_WITHOUT_PARAMS = '''[logconf]
foo: bar
'''

INI_EMPTY = '[logconf]'

INI_INVALID = 'def[ault]'

class TestIniLoader(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=INI_WITH_PARAMS)
    def test_load_with_ini_having_params(self, func): # pylint: disable=unused-argument
        with open('somelogconf.ini', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == INI_WITH_PARAMS
        conf = load('somelogconf.ini')
        self.assertEqual(conf['datefmt'], '%Y')
        self.assertEqual(conf['filename'], 'somelogconf.log')
        self.assertEqual(conf['filemode'], 'w')
        self.assertEqual(conf['format'], 'Some Log %(asctime)s')
        self.assertEqual(conf['level'], 'critical')

    @patch('builtins.open', new_callable=mock_open, read_data=INI_WITHOUT_PARAMS)
    def test_load_with_ini_not_having_params(self, func): # pylint: disable=unused-argument
        with open('somelogconf.ini', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == INI_WITHOUT_PARAMS
        conf = load('somelogconf.ini')
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('filemode' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)

    @patch('builtins.open', new_callable=mock_open, read_data=INI_EMPTY)
    def test_load_with_empty_ini(self, func): # pylint: disable=unused-argument
        with open('somelogconf.ini', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == INI_EMPTY
        conf = load('somelogconf.ini')
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('filemode' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)

    @patch('builtins.open', new_callable=mock_open, read_data=INI_INVALID)
    def test_load_with_invalid_ini(self, func): # pylint: disable=unused-argument
        with open('somelogconf.ini', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == INI_INVALID
        with self.assertRaises(configparser.MissingSectionHeaderError):
            load('somelogconf.ini')
