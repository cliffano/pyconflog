# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
from unittest.mock import patch
import unittest.mock
import unittest
import os
from logconf.loaders.environ_loader import load

ENVIRON_WITH_PARAMS = {
    'LOGCONF_DATEFMT': '%Y',
    'LOGCONF_FILENAME': 'somelogconf.log',
    'LOGCONF_FORMAT': 'Some Log %(asctime)s',
    'LOGCONF_LEVEL': 'critical'
}

ENVIRON_WITHOUT_PARAMS = {
    'LOGCONF_FOO': 'bar'
}

ENVIRON_EMPTY = {}

class TestEnviron(unittest.TestCase):

    @patch.dict(os.environ, ENVIRON_WITH_PARAMS, clear=True)
    def test_load_with_environ_having_params(self):
        conf = load()
        self.assertEqual(conf['datefmt'], '%Y')
        self.assertEqual(conf['filename'], 'somelogconf.log')
        self.assertEqual(conf['format'], 'Some Log %(asctime)s')
        self.assertEqual(conf['level'], 'critical')

    @patch.dict(os.environ, ENVIRON_WITHOUT_PARAMS, clear=True)
    def test_load_with_environ_not_having_params(self):
        conf = load()
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)

    @patch.dict(os.environ, ENVIRON_EMPTY, clear=True)
    def test_load_with_empty_environ(self):
        conf = load()
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)
