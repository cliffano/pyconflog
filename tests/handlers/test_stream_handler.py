# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from unittest.mock import patch
import unittest.mock
import unittest
import logging
from conflog.handlers.stream_handler import init

class TestStreamHandler(unittest.TestCase):

    @patch('logging.StreamHandler.__new__')
    @patch('logging.Formatter.__new__')
    def test_init( # pylint: disable=unused-argument
            self,
            func_formatter,
            func_stream_handler):

        mock_config = unittest.mock.Mock()
        mock_config.get_datefmt.return_value = '%d-%b-%y %H:%M:%S'
        mock_config.get_level.return_value = logging.INFO
        mock_config.get_format.return_value = '%(asctime)s --> '\
                                              '%(name)s - %(levelname)s - %(message)s'

        mock_formatter = unittest.mock.Mock()
        func_formatter.return_value = mock_formatter

        mock_stream_handler = unittest.mock.Mock()
        func_stream_handler.return_value = mock_stream_handler

        result = init(mock_config)
        self.assertEqual(result, mock_stream_handler)
        mock_stream_handler.setFormatter.assert_called_once_with(mock_formatter)
        mock_stream_handler.setLevel.assert_called_once_with(logging.INFO)
