# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from unittest.mock import patch
import unittest.mock
import unittest
import os
from conflog.loaders.environ_loader import load

ENVIRON_WITH_PARAMS = {
    'CONFLOG_DATEFMT': '%Y',
    'CONFLOG_FILENAME': 'someconflog.log',
    'CONFLOG_FILEMODE': 'w',
    'CONFLOG_FORMAT': '%(some_extra1)s Some Log %(asctime)s',
    'CONFLOG_LEVEL': 'critical',
    'CONFLOG_EXTRAS': 'some_extra1=some_value1,some_extra2=some_value2'
}

ENVIRON_WITHOUT_PARAMS = {
    'CONFLOG_FOO': 'bar'
}

ENVIRON_EMPTY = {}

class TestEnvironLoader(unittest.TestCase):

    @patch.dict(os.environ, ENVIRON_WITH_PARAMS, clear=True)
    def test_load_with_environ_having_params(self):
        conf = load()
        self.assertEqual(conf['datefmt'], '%Y')
        self.assertEqual(conf['filename'], 'someconflog.log')
        self.assertEqual(conf['filemode'], 'w')
        self.assertEqual(conf['format'], '%(some_extra1)s Some Log %(asctime)s')
        self.assertEqual(conf['level'], 'critical')
        self.assertEqual(conf['extras'], 'some_extra1=some_value1,some_extra2=some_value2')

    @patch.dict(os.environ, ENVIRON_WITHOUT_PARAMS, clear=True)
    def test_load_with_environ_not_having_params(self):
        conf = load()
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('filemode' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)
        self.assertFalse('extras' in conf)

    @patch.dict(os.environ, ENVIRON_EMPTY, clear=True)
    def test_load_with_empty_environ(self):
        conf = load()
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('filemode' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)
        self.assertFalse('extras' in conf)
