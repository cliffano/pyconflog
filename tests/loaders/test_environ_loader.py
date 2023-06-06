# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from unittest.mock import patch
import unittest.mock
import unittest
import os
from logconf.loaders.environ_loader import load

ENVIRON_WITH_PARAMS = {
    'LOGCONF_DATEFMT': '%Y',
    'LOGCONF_FILENAME': 'somelogconf.log',
    'LOGCONF_FILEMODE': 'w',
    'LOGCONF_FORMAT': '%(some_extra1)s Some Log %(asctime)s',
    'LOGCONF_LEVEL': 'critical',
    'LOGCONF_EXTRAS': 'some_extra1=some_value1,some_extra2=some_value2'
}

ENVIRON_WITHOUT_PARAMS = {
    'LOGCONF_FOO': 'bar'
}

ENVIRON_EMPTY = {}

class TestEnvironLoader(unittest.TestCase):

    @patch.dict(os.environ, ENVIRON_WITH_PARAMS, clear=True)
    def test_load_with_environ_having_params(self):
        conf = load()
        self.assertEqual(conf['datefmt'], '%Y')
        self.assertEqual(conf['filename'], 'somelogconf.log')
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
