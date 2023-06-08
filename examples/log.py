# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from conflog import Conflog

cfl = Conflog(conf_files=['conflog.yaml'])

logger1 = cfl.get_logger('foobar1')
logger1.critical('Some critical message')

logger2 = cfl.get_logger('foobar2')
logger2.warning('Some warning message')
