# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
from unittest.mock import patch, mock_open
import unittest.mock
import unittest
import json
from logconf.loaders.json_loader import load

JSON_WITH_PARAMS = '''{
    "datefmt": "%Y",
    "filename": "somelogconf.log",
    "filemode": "w",
    "format": "Some Log %(asctime)s",
    "level": "critical"
}'''

JSON_WITHOUT_PARAMS = '''{
    "foo": "bar"
}'''

JSON_EMPTY = '{}'

JSON_INVALID = '---\nhello'

class TestJsonLoader(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=JSON_WITH_PARAMS)
    def test_load_with_json_having_params(self, func): # pylint: disable=unused-argument
        with open('somelogconf.json', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == JSON_WITH_PARAMS
        conf = load('somelogconf.json')
        self.assertEqual(conf['datefmt'], '%Y')
        self.assertEqual(conf['filename'], 'somelogconf.log')
        self.assertEqual(conf['filemode'], 'w')
        self.assertEqual(conf['format'], 'Some Log %(asctime)s')
        self.assertEqual(conf['level'], 'critical')

    @patch('builtins.open', new_callable=mock_open, read_data=JSON_WITHOUT_PARAMS)
    def test_load_with_json_not_having_params(self, func): # pylint: disable=unused-argument
        with open('somelogconf.json', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == JSON_WITHOUT_PARAMS
        conf = load('somelogconf.json')
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('filemode' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)

    @patch('builtins.open', new_callable=mock_open, read_data=JSON_EMPTY)
    def test_load_with_empty_json(self, func): # pylint: disable=unused-argument
        with open('somelogconf.json', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == JSON_EMPTY
        conf = load('somelogconf.json')
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('filemode' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)

    @patch('builtins.open', new_callable=mock_open, read_data=JSON_INVALID)
    def test_load_with_invalid_json(self, func): # pylint: disable=unused-argument
        with open('somelogconf.json', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == JSON_INVALID
        with self.assertRaises(json.decoder.JSONDecodeError):
            load('somelogconf.json')
