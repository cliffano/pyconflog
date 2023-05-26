# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code
from unittest.mock import patch, mock_open
import unittest.mock
import unittest
import xml
from logconf.loaders.xml_loader import load

XML_WITH_PARAMS = '''<?xml version="1.0" encoding="UTF-8"?>
<logconf>
  <datefmt>%Y</datefmt>
  <filename>somelogconf.log</filename>
  <filemode>w</filemode>
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

class TestXmlLoader(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=XML_WITH_PARAMS)
    def test_load_with_xml_having_params(self, func): # pylint: disable=unused-argument
        with open('somelogconf.xml', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == XML_WITH_PARAMS
        conf = load('somelogconf.xml')
        self.assertEqual(conf['datefmt'], '%Y')
        self.assertEqual(conf['filename'], 'somelogconf.log')
        self.assertEqual(conf['filemode'], 'w')
        self.assertEqual(conf['format'], 'Some Log %(asctime)s')
        self.assertEqual(conf['level'], 'critical')

    @patch('builtins.open', new_callable=mock_open, read_data=XML_WITHOUT_PARAMS)
    def test_load_with_xml_not_having_params(self, func): # pylint: disable=unused-argument
        with open('somelogconf.xml', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == XML_WITHOUT_PARAMS
        conf = load('somelogconf.xml')
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('filemode' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)

    @patch('builtins.open', new_callable=mock_open, read_data=XML_EMPTY)
    def test_load_with_empty_xml(self, func): # pylint: disable=unused-argument
        with open('somelogconf.xml', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == XML_EMPTY
        conf = load('somelogconf.xml')
        self.assertFalse('datefmt' in conf)
        self.assertFalse('filename' in conf)
        self.assertFalse('filemode' in conf)
        self.assertFalse('format' in conf)
        self.assertFalse('level' in conf)

    @patch('builtins.open', new_callable=mock_open, read_data=XML_INVALID)
    def test_load_with_invalid_xml(self, func): # pylint: disable=unused-argument
        with open('somelogconf.xml', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == XML_INVALID
        with self.assertRaises(xml.etree.ElementTree.ParseError):
            load('somelogconf.xml')
