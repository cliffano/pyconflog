# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
import unittest
from logconf.logconf import (
    get_logger,
)

class TestJsonConf(unittest.TestCase):

    def test_get_logger_with_single_conf_file(self): # pylint: disable=unused-argument
        logger = get_logger('someloggername',
                            conf_files=['tests-integration/fixtures/logconf.json'])
        logger.info('Some log message for JSON integration test')
