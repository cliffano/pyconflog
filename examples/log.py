# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from logconf import Logconf

lc = Logconf(conf_files=['logconf.yaml'])

logger1 = lc.get_logger('foobar1')
logger1.critical('Some critical message')

logger2 = lc.get_logger('foobar2')
logger2.warning('Some warning message')
