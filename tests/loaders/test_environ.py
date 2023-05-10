from logconf.loaders.environ import load
import os
import unittest
import unittest.mock
from unittest.mock import patch

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

    @unittest.mock.patch.dict(os.environ, ENVIRON_WITH_PARAMS, clear=True)
    def test_load_with_environ_having_params(self):
        conf = load()
        self.assertEqual(conf['datefmt'], '%Y')
        self.assertEqual(conf['filename'], 'somelogconf.log')
        self.assertEqual(conf['format'], 'Some Log %(asctime)s')
        self.assertEqual(conf['level'], 'critical')

    @unittest.mock.patch.dict(os.environ, ENVIRON_WITHOUT_PARAMS, clear=True)
    def test_load_with_environ_not_having_params(self):
        conf = load()
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)

    @unittest.mock.patch.dict(os.environ, ENVIRON_EMPTY, clear=True)
    def test_load_with_empty_environ(self):
        conf = load()
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)

if __name__ == '__main__':
    unittest.main()