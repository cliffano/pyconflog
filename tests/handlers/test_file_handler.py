# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from unittest.mock import patch
import unittest.mock
import unittest
import logging
from conflog.handlers.file_handler import init

class TestFileHandler(unittest.TestCase):

    @patch('logging.FileHandler.__new__')
    @patch('logging.Formatter.__new__')
    def test_init( # pylint: disable=unused-argument
            self,
            func_formatter,
            func_file_handler):

        mock_config = unittest.mock.Mock()
        mock_config.get_datefmt.return_value = '%d-%b-%y %H:%M:%S'
        mock_config.get_level.return_value = logging.INFO
        mock_config.get_format.return_value = '%(asctime)s --> '\
                                              '%(name)s - %(levelname)s - %(message)s'
        mock_config.get_filename.return_value = 'conflog.log'
        mock_config.get_filemode.return_value = 'w'

        mock_formatter = unittest.mock.Mock()
        func_formatter.return_value = mock_formatter

        mock_file_handler = unittest.mock.Mock()
        func_file_handler.return_value = mock_file_handler

        result = init(mock_config)
        self.assertEqual(result, mock_file_handler)
        mock_file_handler.setFormatter.assert_called_once_with(mock_formatter)
        mock_file_handler.setLevel.assert_called_once_with(logging.INFO)
