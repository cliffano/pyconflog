# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from unittest.mock import patch, mock_open
import unittest.mock
import unittest
import configparser
from conflog.loaders.ini_loader import load

INI_WITH_PARAMS = '''[conflog]
datefmt: %%Y
filename: someconflog.log
filemode: w
format: %%(some_extra1)s Some Log %%(asctime)s
level: critical
extras: some_extra1=some_value1,some_extra2=some_value2
'''

INI_WITHOUT_PARAMS = '''[conflog]
foo: bar
'''

INI_EMPTY = '[conflog]'

INI_INVALID = 'def[ault]'

class TestIniLoader(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=INI_WITH_PARAMS)
    def test_load_with_ini_having_params(self, func): # pylint: disable=unused-argument
        with open('someconflog.ini', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == INI_WITH_PARAMS
        conf = load('someconflog.ini')
        self.assertEqual(conf['datefmt'], '%Y')
        self.assertEqual(conf['filename'], 'someconflog.log')
        self.assertEqual(conf['filemode'], 'w')
        self.assertEqual(conf['format'], '%(some_extra1)s Some Log %(asctime)s')
        self.assertEqual(conf['level'], 'critical')
        self.assertEqual(conf['extras'], 'some_extra1=some_value1,some_extra2=some_value2')

    @patch('builtins.open', new_callable=mock_open, read_data=INI_WITHOUT_PARAMS)
    def test_load_with_ini_not_having_params(self, func): # pylint: disable=unused-argument
        with open('someconflog.ini', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == INI_WITHOUT_PARAMS
        conf = load('someconflog.ini')
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('filemode' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)
        self.assertFalse('extras' in conf)

    @patch('builtins.open', new_callable=mock_open, read_data=INI_EMPTY)
    def test_load_with_empty_ini(self, func): # pylint: disable=unused-argument
        with open('someconflog.ini', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == INI_EMPTY
        conf = load('someconflog.ini')
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('filemode' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)
        self.assertFalse('extras' in conf)

    @patch('builtins.open', new_callable=mock_open, read_data=INI_INVALID)
    def test_load_with_invalid_ini(self, func): # pylint: disable=unused-argument
        with open('someconflog.ini', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == INI_INVALID
        with self.assertRaises(configparser.MissingSectionHeaderError):
            load('someconflog.ini')
