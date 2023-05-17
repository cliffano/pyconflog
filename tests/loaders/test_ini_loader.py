import configparser
from logconf.loaders.ini_loader import load
import unittest
import unittest.mock
from unittest.mock import patch, mock_open

INI_WITH_PARAMS = '''[logconf]
datefmt: %%Y
filename: somelogconf.log
format: Some Log %%(asctime)s
level: critical
'''

INI_WITHOUT_PARAMS = '''[logconf]
foo: bar
'''

INI_EMPTY = '[logconf]'

INI_INVALID = 'def[ault]'

class TestIni(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=INI_WITH_PARAMS)
    def test_load_with_ini_having_params(self, func):
        assert open('somelogconf.ini').read() == INI_WITH_PARAMS
        conf = load('somelogconf.ini')
        self.assertEqual(conf['datefmt'], '%Y')
        self.assertEqual(conf['filename'], 'somelogconf.log')
        self.assertEqual(conf['format'], 'Some Log %(asctime)s')
        self.assertEqual(conf['level'], 'critical')

    @patch('builtins.open', new_callable=mock_open, read_data=INI_WITHOUT_PARAMS)
    def test_load_with_ini_not_having_params(self, func):
        assert open('somelogconf.ini').read() == INI_WITHOUT_PARAMS
        conf = load('somelogconf.ini')
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)

    @patch('builtins.open', new_callable=mock_open, read_data=INI_EMPTY)
    def test_load_with_empty_ini(self, func):
        assert open('somelogconf.ini').read() == INI_EMPTY
        conf = load('somelogconf.ini')
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)

    @patch('builtins.open', new_callable=mock_open, read_data=INI_INVALID)
    def test_load_with_invalid_ini(self, func):
        assert open('somelogconf.ini').read() == INI_INVALID
        with self.assertRaises(configparser.MissingSectionHeaderError):
            conf = load('somelogconf.ini')

if __name__ == '__main__':
    unittest.main()