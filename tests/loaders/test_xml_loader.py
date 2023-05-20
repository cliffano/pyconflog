import pytest
from logconf.loaders.xml_loader import load
import unittest
from unittest.mock import patch, mock_open
import xml

XML_WITH_PARAMS = '''<?xml version="1.0" encoding="UTF-8"?>
<logconf>
  <datefmt>%Y</datefmt>
  <filename>somelogconf.log</filename>
  <format>Some Log %(asctime)s</format>
  <level>critical</level>
</logconf>
'''

XML_WITHOUT_PARAMS = '''<?xml version="1.0" encoding="UTF-8"?>
<logconf>
  <foo>bar</foo>
</logconf>
'''

XML_EMPTY = '<?xml version="1.0" encoding="UTF-8"?><logconf></logconf>'

XML_INVALID = '>%%%{foobar}!!!<'

class TestXml(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=XML_WITH_PARAMS)
    def test_load_with_xml_having_params(self, func):
        assert open('somelogconf.xml').read() == XML_WITH_PARAMS
        conf = load('somelogconf.xml')
        self.assertEqual(conf['datefmt'], '%Y')
        self.assertEqual(conf['filename'], 'somelogconf.log')
        self.assertEqual(conf['format'], 'Some Log %(asctime)s')
        self.assertEqual(conf['level'], 'critical')

    @patch('builtins.open', new_callable=mock_open, read_data=XML_WITHOUT_PARAMS)
    def test_load_with_xml_not_having_params(self, func):
        assert open('somelogconf.xml').read() == XML_WITHOUT_PARAMS
        conf = load('somelogconf.xml')
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)

    @patch('builtins.open', new_callable=mock_open, read_data=XML_EMPTY)
    def test_load_with_empty_XML(self, func):
        assert open('somelogconf.xml').read() == XML_EMPTY
        conf = load('somelogconf.xml')
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)

    @patch('builtins.open', new_callable=mock_open, read_data=XML_INVALID)
    def test_load_with_invalid_XML(self, func):
        assert open('somelogconf.xml').read() == XML_INVALID
        with self.assertRaises(xml.etree.ElementTree.ParseError):
            conf = load('somelogconf.xml')
