# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from conflog import Conflog

cfl1 = Conflog(conf_files=["conflog.yaml"])

logger1a = cfl1.get_logger("foobar1a")
logger1a.critical("Some critical message 1a")

logger1b = cfl1.get_logger("foobar1b")
logger1b.warning("Some warning message 1b")

cfl2 = Conflog(["conflog.yaml"])

logger2a = cfl2.get_logger("foobar2a")
logger2a.critical("Some critical message 2a")

logger2b = cfl2.get_logger("foobar2b")
logger2b.warning("Some warning message 2b")

cfl3 = Conflog("conflog.yaml")

logger3a = cfl3.get_logger("foobar3a")
logger3a.critical("Some critical message 3a")

logger3b = cfl3.get_logger("foobar3b")
logger3b.warning("Some warning message 3b")
