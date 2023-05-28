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
    @patch('logging.basicConfig')
    @patch('logging.getLogger')
    def test_logconf( # pylint: disable=too-many-arguments
            self,
            func_get_logger,
            func_basic_config,
            func_stream_handler,
            func_file_handler,
            func_config):

        mock_config = unittest.mock.Mock()
        mock_stream_handler = unittest.mock.Mock()
        mock_file_handler = unittest.mock.Mock()
        mock_logger = unittest.mock.Mock()

        func_config.return_value = mock_config
        func_stream_handler.return_value = mock_stream_handler
        func_file_handler.return_value = mock_file_handler
        func_get_logger.return_value = mock_logger

        mock_config.get_handlers.return_value = ['stream', 'file']
        mock_config.get_datefmt.return_value = '%d-%b-%y %H:%M:%S'
        mock_config.get_filename.return_value = 'logconf.log'
        mock_config.get_filemode.return_value = 'w'
        mock_config.get_format.return_value = '%(asctime)s --> '\
                                              '%(name)s - %(levelname)s - %(message)s'
        mock_config.get_level.return_value = logging.INFO

        logconf = Logconf(conf_files=['somefile.ini', 'somefile.json'])
        logger = logconf.get_logger('someloggername')
        self.assertEqual(logger, mock_logger)

        func_basic_config.assert_called_once_with(
            datefmt='%d-%b-%y %H:%M:%S',
            level=logging.INFO,
        )
        func_get_logger.assert_called_once_with('someloggername')
