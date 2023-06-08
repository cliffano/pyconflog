# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from unittest.mock import patch, mock_open
import unittest.mock
import unittest
import json
from conflog.loaders.json_loader import load

JSON_WITH_PARAMS = '''{
    "datefmt": "%Y",
    "filename": "someconflog.log",
    "filemode": "w",
    "format": "%(some_extra1)s Some Log %(asctime)s",
    "level": "critical",
    "extras": {
        "some_extra1": "some_value1",
        "some_extra2": "some_value2"
    }
}'''

JSON_WITHOUT_PARAMS = '''{
    "foo": "bar"
}'''

JSON_EMPTY = '{}'

JSON_INVALID = '---\nhello'

class TestJsonLoader(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=JSON_WITH_PARAMS)
    def test_load_with_json_having_params(self, func): # pylint: disable=unused-argument
        with open('someconflog.json', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == JSON_WITH_PARAMS
        conf = load('someconflog.json')
        self.assertEqual(conf['datefmt'], '%Y')
        self.assertEqual(conf['filename'], 'someconflog.log')
        self.assertEqual(conf['filemode'], 'w')
        self.assertEqual(conf['format'], '%(some_extra1)s Some Log %(asctime)s')
        self.assertEqual(conf['level'], 'critical')
        extras = conf['extras']
        self.assertEqual(len(extras.keys()), 2)
        self.assertEqual(extras['some_extra1'], 'some_value1')
        self.assertEqual(extras['some_extra2'], 'some_value2')

    @patch('builtins.open', new_callable=mock_open, read_data=JSON_WITHOUT_PARAMS)
    def test_load_with_json_not_having_params(self, func): # pylint: disable=unused-argument
        with open('someconflog.json', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == JSON_WITHOUT_PARAMS
        conf = load('someconflog.json')
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('filemode' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)
        self.assertFalse('extras' in conf)

    @patch('builtins.open', new_callable=mock_open, read_data=JSON_EMPTY)
    def test_load_with_empty_json(self, func): # pylint: disable=unused-argument
        with open('someconflog.json', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == JSON_EMPTY
        conf = load('someconflog.json')
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('filemode' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)
        self.assertFalse('extras' in conf)

    @patch('builtins.open', new_callable=mock_open, read_data=JSON_INVALID)
    def test_load_with_invalid_json(self, func): # pylint: disable=unused-argument
        with open('someconflog.json', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == JSON_INVALID
        with self.assertRaises(json.decoder.JSONDecodeError):
            load('someconflog.json')
