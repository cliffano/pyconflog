# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from unittest.mock import patch, mock_open
import unittest.mock
import unittest
import xml
from conflog.loaders.xml_loader import load

XML_WITH_PARAMS = '''<?xml version="1.0" encoding="UTF-8"?>
<conflog>
  <datefmt>%Y</datefmt>
  <filename>someconflog.log</filename>
  <filemode>w</filemode>
  <format>%(some_extra1)s Some Log %(asctime)s</format>
  <level>critical</level>
  <extras>some_extra1=some_value1,some_extra2=some_value2</extras>
</conflog>
'''

XML_WITHOUT_PARAMS = '''<?xml version="1.0" encoding="UTF-8"?>
<conflog>
  <foo>bar</foo>
</conflog>
'''

XML_EMPTY = '<?xml version="1.0" encoding="UTF-8"?><conflog></conflog>'

XML_INVALID = '>%%%{foobar}!!!<'

class TestXmlLoader(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=XML_WITH_PARAMS)
    def test_load_with_xml_having_params(self, func): # pylint: disable=unused-argument
        with open('someconflog.xml', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == XML_WITH_PARAMS
        conf = load('someconflog.xml')
        self.assertEqual(conf['datefmt'], '%Y')
        self.assertEqual(conf['filename'], 'someconflog.log')
        self.assertEqual(conf['filemode'], 'w')
        self.assertEqual(conf['format'], '%(some_extra1)s Some Log %(asctime)s')
        self.assertEqual(conf['level'], 'critical')
        self.assertEqual(conf['extras'], 'some_extra1=some_value1,some_extra2=some_value2')

    @patch('builtins.open', new_callable=mock_open, read_data=XML_WITHOUT_PARAMS)
    def test_load_with_xml_not_having_params(self, func): # pylint: disable=unused-argument
        with open('someconflog.xml', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == XML_WITHOUT_PARAMS
        conf = load('someconflog.xml')
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('filemode' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)
        self.assertFalse('extras' in conf)

    @patch('builtins.open', new_callable=mock_open, read_data=XML_EMPTY)
    def test_load_with_empty_xml(self, func): # pylint: disable=unused-argument
        with open('someconflog.xml', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == XML_EMPTY
        conf = load('someconflog.xml')
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('filemode' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)
        self.assertFalse('extras' in conf)

    @patch('builtins.open', new_callable=mock_open, read_data=XML_INVALID)
    def test_load_with_invalid_xml(self, func): # pylint: disable=unused-argument
        with open('someconflog.xml', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == XML_INVALID
        with self.assertRaises(xml.etree.ElementTree.ParseError):
            load('someconflog.xml')
