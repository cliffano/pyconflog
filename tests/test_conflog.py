# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from unittest.mock import patch
import unittest.mock
import unittest
import logging
from conflog import Conflog

class TestConflog(unittest.TestCase):

    @patch('conflog.config.Config.__new__')
    @patch('logging.FileHandler.__new__')
    @patch('logging.StreamHandler.__new__')
    @patch('logging.Formatter.__new__')
    @patch('logging.basicConfig')
    @patch('logging.getLogger')
    @patch('logging.LoggerAdapter.__new__')
    def test_conflog( # pylint: disable=too-many-arguments
            self,
            func_logger_adapter,
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
        mock_adapted_logger = unittest.mock.Mock()
        mock_logger.handlers = [mock_stream_handler, mock_file_handler]

        func_config.return_value = mock_config
        func_stream_handler.return_value = mock_stream_handler
        func_file_handler.return_value = mock_file_handler
        func_formatter.return_value = mock_formatter
        func_get_logger.return_value = mock_logger
        func_logger_adapter.return_value = mock_adapted_logger

        mock_config.get_handlers.return_value = ['stream', 'file']
        mock_config.get_datefmt.return_value = '%d-%b-%y %H:%M:%S'
        mock_config.get_level.return_value = logging.INFO

        conflog = Conflog(
            conf_files=['somefile.ini', 'somefile.json'],
            conf_dict={'format': '[SOMEAPP] %(message)s'}
        )
        mock_stream_handler.setFormatter.assert_called_once_with(mock_formatter)
        mock_stream_handler.setLevel.assert_called_once_with(logging.INFO)
        mock_file_handler.setFormatter.assert_called_once_with(mock_formatter)
        mock_file_handler.setLevel.assert_called_once_with(logging.INFO)
        func_basic_config.assert_called_once_with(
            datefmt='%d-%b-%y %H:%M:%S',
            level=logging.INFO,
        )

        logger = conflog.get_logger('someloggername')
        func_get_logger.assert_called_with('someloggername')
        self.assertEqual(logger, mock_adapted_logger)
        self.assertFalse(mock_logger.propagate)

        # should add configured handlers
        mock_logger.addHandler.assert_any_call(mock_stream_handler)
        mock_logger.addHandler.assert_any_call(mock_file_handler)

        # should set configured log level
        mock_adapted_logger.setLevel.assert_called_once_with(logging.INFO)

        conflog.close_logger_handlers('someloggername')
        # should close configured handlers
        mock_stream_handler.close.assert_called_once_with()
        mock_file_handler.close.assert_called_once_with()

        config = conflog.get_config_properties()
        # should retrieve the correct configuration
        self.assertEqual(config, mock_config.conf)
