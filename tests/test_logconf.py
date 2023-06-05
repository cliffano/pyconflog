# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code
from unittest.mock import patch
import unittest.mock
import unittest
import logging
from logconf.logconf import Logconf

class TestLogconf(unittest.TestCase):

    @patch('logconf.config.Config.__new__')
    @patch('logging.FileHandler.__new__')
    @patch('logging.StreamHandler.__new__')
    @patch('logging.Formatter.__new__')
    @patch('logging.basicConfig')
    @patch('logging.getLogger')
    def test_logconf( # pylint: disable=too-many-arguments
            self,
            func_get_logger,
            func_basic_config,
            func_formatter,
            func_stream_handler,
            func_file_handler,
            func_config):

        mock_config = unittest.mock.Mock()
        mock_stream_handler = unittest.mock.Mock()
        mock_file_handler = unittest.mock.Mock()
        mock_formatter = unittest.mock.Mock()
        mock_logger = unittest.mock.Mock()
        mock_logger.handlers = [mock_stream_handler, mock_file_handler]

        func_config.return_value = mock_config
        func_stream_handler.return_value = mock_stream_handler
        func_file_handler.return_value = mock_file_handler
        func_formatter.return_value = mock_formatter
        func_get_logger.return_value = mock_logger

        mock_config.get_handlers.return_value = ['stream', 'file']
        mock_config.get_datefmt.return_value = '%d-%b-%y %H:%M:%S'
        mock_config.get_level.return_value = logging.INFO

        logconf = Logconf(conf_files=['somefile.ini', 'somefile.json'])
        logger = logconf.get_logger('someloggername')
        self.assertEqual(logger, mock_logger)
        logconf.close_logger_handlers('someloggername')

        mock_stream_handler.setFormatter.assert_called_once_with(mock_formatter)
        mock_file_handler.setFormatter.assert_called_once_with(mock_formatter)

        func_basic_config.assert_called_once_with(
            datefmt='%d-%b-%y %H:%M:%S',
            level=logging.INFO,
        )

        func_get_logger.assert_called_with('someloggername')
        mock_logger.addHandler.assert_any_call(mock_stream_handler)
        mock_logger.addHandler.assert_any_call(mock_file_handler)
        mock_stream_handler.close.assert_called_once_with()
        mock_file_handler.close.assert_called_once_with()
