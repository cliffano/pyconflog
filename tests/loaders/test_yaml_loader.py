import pytest
from logconf.loaders.yaml_loader import load
import unittest
from unittest.mock import patch, mock_open
import yaml

YAML_WITH_PARAMS = '''---
datefmt: "%Y"
filename: "somelogconf.log"
format: "Some Log %(asctime)s"
level: "critical"
'''

YAML_WITHOUT_PARAMS = '''---
foo: "bar"
'''

YAML_EMPTY = '---'

YAML_INVALID = '%%%{foobar}!!!'

class TestYamlLoader(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=YAML_WITH_PARAMS)
    def test_load_with_yaml_having_params(self, func):
        assert open('somelogconf.yaml').read() == YAML_WITH_PARAMS
        conf = load('somelogconf.yaml')
        self.assertEqual(conf['datefmt'], '%Y')
        self.assertEqual(conf['filename'], 'somelogconf.log')
        self.assertEqual(conf['format'], 'Some Log %(asctime)s')
        self.assertEqual(conf['level'], 'critical')

    @patch('builtins.open', new_callable=mock_open, read_data=YAML_WITHOUT_PARAMS)
    def test_load_with_yaml_not_having_params(self, func):
        assert open('somelogconf.yaml').read() == YAML_WITHOUT_PARAMS
        conf = load('somelogconf.yaml')
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)

    @patch('builtins.open', new_callable=mock_open, read_data=YAML_EMPTY)
    def test_load_with_empty_YAML(self, func):
        assert open('somelogconf.yaml').read() == YAML_EMPTY
        conf = load('somelogconf.yaml')
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)

    @patch('builtins.open', new_callable=mock_open, read_data=YAML_INVALID)
    def test_load_with_invalid_YAML(self, func):
        assert open('somelogconf.yaml').read() == YAML_INVALID
        with self.assertRaises(yaml.scanner.ScannerError):
            conf = load('somelogconf.yaml')
