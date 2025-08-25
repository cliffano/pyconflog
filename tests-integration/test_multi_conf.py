# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest
import os
import os.path
from conflog import Conflog


class TestMultiConf(unittest.TestCase):

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
        self.log_file = None

    # close handlers and remove log file on tearDown
    def tearDown(self):
        self.conflog.close_logger_handlers(self.logger_name)
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_get_logger_with_multi_conf_files(self):
        # should have yaml log file since yaml config is last in the conf_files
        self.log_file = "stage/test-integration/test-yaml-conf.log"
        self.logger_name = "test_get_logger_with_multi_conf_files"
        self.conflog = Conflog(
            conf_files=[
                "tests-integration/fixtures/conflog.ini",
                "tests-integration/fixtures/conflog.json",
                "tests-integration/fixtures/conflog.xml",
                "tests-integration/fixtures/conflog.yaml",
            ]
        )
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
        # should have YAML-CONFLOG in the log message because yaml config is last in the conf_files
        self.assertEqual(
            content,
            "[YAML-CONFLOG] [someenv-someid] INFO Some info log message\n"
            "[YAML-CONFLOG] [someenv-someid] WARNING Some warning log message\n"
            "[YAML-CONFLOG] [someenv-someid] ERROR Some error log message\n"
            "[YAML-CONFLOG] [someenv-someid] CRITICAL Some critical log message\n",
        )

    def test_get_logger_with_multi_conf_files_reversed(self):
        # should have ini log file since ini config is last in the conf_files
        self.log_file = "stage/test-integration/test-ini-conf.log"
        self.logger_name = "test_get_logger_with_multi_conf_files"
        self.conflog = Conflog(
            conf_files=[
                "tests-integration/fixtures/conflog.yaml",
                "tests-integration/fixtures/conflog.xml",
                "tests-integration/fixtures/conflog.json",
                "tests-integration/fixtures/conflog.ini",
            ]
        )
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
        # should have INI-CONFLOG in the log message because ini config is last in the conf_files
        self.assertEqual(
            content,
            "[INI-CONFLOG] [someenv-someid] INFO Some info log message\n"
            "[INI-CONFLOG] [someenv-someid] WARNING Some warning log message\n"
            "[INI-CONFLOG] [someenv-someid] ERROR Some error log message\n"
            "[INI-CONFLOG] [someenv-someid] CRITICAL Some critical log message\n",
        )

    def test_get_logger_with_multi_conf_files_envvar_override(self):
        # should have yaml log file since yaml config is last in the conf_files
        self.log_file = "stage/test-integration/test-yaml-conf.log"
        self.logger_name = "test_get_logger_with_multi_conf_files"
        os.environ["CONFLOG_FORMAT"] = (
            "[ENVVAR-CONFLOG] [%(env)s-%(id)s] %(levelname)s %(message)s"
        )
        self.conflog = Conflog(
            conf_files=[
                "tests-integration/fixtures/conflog.ini",
                "tests-integration/fixtures/conflog.json",
                "tests-integration/fixtures/conflog.xml",
                "tests-integration/fixtures/conflog.yaml",
            ]
        )
        logger = self.conflog.get_logger(self.logger_name)
        os.unsetenv("CONFLOG_FORMAT")
        if "CONFLOG_FORMAT" in os.environ:
            os.environ.pop("CONFLOG_FORMAT")
        logger.debug("Some debug log message")
        logger.info("Some info log message")
        logger.warning("Some warning log message")
        logger.error("Some error log message")
        logger.critical("Some critical log message")
        with open(self.log_file, "r", encoding="utf-8") as stream:
            content = stream.read()
        # should exclude debug
        # should include info, warning, error, critical
        # should have ENVVAR-CONFLOG in the log message
        # because CONFLOG_FORMAT overrides all conf_files
        self.assertEqual(
            content,
            "[ENVVAR-CONFLOG] [someenv-someid] INFO Some info log message\n"
            "[ENVVAR-CONFLOG] [someenv-someid] WARNING Some warning log message\n"
            "[ENVVAR-CONFLOG] [someenv-someid] ERROR Some error log message\n"
            "[ENVVAR-CONFLOG] [someenv-someid] CRITICAL Some critical log message\n",
        )
