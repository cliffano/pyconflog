# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest
import os
import os.path
from conflog import Conflog


class TestIniConf(unittest.TestCase):

    def setUp(self):
        os.unsetenv("CONFLOG_HANDLERS")
        if "CONFLOG_HANDLERS" in os.environ:
            os.environ.pop("CONFLOG_HANDLERS")
        os.unsetenv("CONFLOG_DATEFMT")
        if "CONFLOG_DATEFMT" in os.environ:
            os.environ.pop("CONFLOG_DATEFMT")
        os.unsetenv("CONFLOG_FORMAT")
        if "CONFLOG_FORMAT" in os.environ:
            os.environ.pop("CONFLOG_FORMAT")
        os.unsetenv("CONFLOG_LEVEL")
        if "CONFLOG_LEVEL" in os.environ:
            os.environ.pop("CONFLOG_LEVEL")
        os.unsetenv("CONFLOG_EXTRAS")
        if "CONFLOG_EXTRAS" in os.environ:
            os.environ.pop("CONFLOG_EXTRAS")
        self.logger_name = None
        self.conflog = None
        self.log_file = "stage/test-integration/test-ini-conf.log"

    # close handlers and remove log file on tearDown
    def tearDown(self):
        self.conflog.close_logger_handlers(self.logger_name)
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_get_logger_with_single_conf_file(self):
        self.logger_name = "test_get_logger_with_single_conf_file"
        self.conflog = Conflog(conf_files=["tests-integration/fixtures/conflog.ini"])
        logger = self.conflog.get_logger(self.logger_name)
        logger.debug("Some debug log message")
        logger.info("Some info log message")
        logger.warning("Some warning log message")
        logger.error("Some error log message")
        logger.critical("Some critical log message")
        with open(self.log_file, "r", encoding="utf-8") as stream:
            content = stream.read()
        # should exclude debug
        # should include info, warning, error, critical
        self.assertEqual(
            content,
            "[INI-CONFLOG] [someenv-someid] INFO Some info log message\n"
            "[INI-CONFLOG] [someenv-someid] WARNING Some warning log message\n"
            "[INI-CONFLOG] [someenv-someid] ERROR Some error log message\n"
            "[INI-CONFLOG] [someenv-someid] CRITICAL Some critical log message\n",
        )

    def test_get_logger_with_single_conf_file_with_excluded_level(self):
        self.logger_name = "test_get_logger_with_single_conf_file_with_excluded_level"
        self.conflog = Conflog(conf_files=["tests-integration/fixtures/conflog.ini"])
        logger = self.conflog.get_logger(self.logger_name)
        logger.debug("Some debug log message")
        with open(self.log_file, "r", encoding="utf-8") as stream:
            content = stream.read()
        # should have empty log message because debug level is excluded
        self.assertEqual(content, "")

    def test_get_logger_with_single_conf_file_with_stream_handler_only(self):
        self.logger_name = "test_get_logger_with_single_conf_file_stream_only"
        self.conflog = Conflog(
            conf_files=["tests-integration/fixtures/conflog-stream-only.ini"]
        )
        logger = self.conflog.get_logger(self.logger_name)
        logger.info("Some info log message")
        # should not create any log file because file handler is not defined
        self.assertFalse(os.path.exists(self.log_file))

    def test_get_logger_with_single_conf_file_with_empty_config(self):
        self.logger_name = "test_get_logger_with_single_conf_file_with_empty_config"
        self.conflog = Conflog(
            conf_files=["tests-integration/fixtures/conflog-empty.ini"]
        )
        logger = self.conflog.get_logger(self.logger_name)
        logger.info("Some info log message")
        # should not create any log file because
        # file handler is not defined in default handlers config
        self.assertFalse(os.path.exists(self.log_file))
