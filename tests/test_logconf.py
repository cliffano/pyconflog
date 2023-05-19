import logconf
import logging
import unittest
import unittest.mock
from unittest.mock import patch, MagicMock
from logconf.logconf import (
    get_logger,
)

class TestLogconf(unittest.TestCase):

    @patch('logconf.config.Config.__new__')
    @patch('logging.basicConfig')
    @patch('logging.getLogger')
    def test_get_logger(
            self,
            func_getLogger,
            func_basicConfig,
            func_config):
        
        
        mock_config = unittest.mock.Mock()
        mock_logger = unittest.mock.Mock()

        func_config.return_value = mock_config
        func_basicConfig.return_value = None
        func_getLogger.return_value = mock_logger

        mock_config.get_datefmt.return_value = '%d-%b-%y %H:%M:%S'
        mock_config.get_filename.return_value = 'logconf.log'
        mock_config.get_filemode.return_value = 'w'
        mock_config.get_format.return_value = '%(asctime)s --> %(name)s - %(levelname)s - %(message)s'
        mock_config.get_level.return_value = logging.INFO
        
        result = logconf.logconf.get_logger('someloggername', conf_files=['somefile.ini', 'somefile.json'])
        self.assertEqual(result, mock_logger)

        func_basicConfig.assert_called_once_with(
            datefmt='%d-%b-%y %H:%M:%S',
            filename='logconf.log',
            filemode='w',
            format='%(asctime)s --> %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        func_getLogger.assert_called_once_with('someloggername')

if __name__ == '__main__':
    unittest.main()
