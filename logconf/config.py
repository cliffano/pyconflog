import logconf
import logging

LEVELS = {
    'debug': logging.DEBUG,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

DEFAULT_DATEFMT = '%d-%b-%y %H:%M:%S'
DEFAULT_FILENAME = 'logconf.log'
DEFAULT_FILEMODE = 'w'
DEFAULT_FORMAT = '%(asctime)s --> %(name)s - %(levelname)s - %(message)s'
DEFAULT_LEVEL = 'info'

class Config():
    """A class for managing logging configurations.
    """

    def __init__(self, conf_files=[]):
        """Initialise config by loading and merging
        the configuration options from files and environment
        variables.
        """

        self.conf = {}

        # Load configurations from files
        for conf_file in conf_files:

            curr_conf = {}

            if (conf_file.endswith('.ini')):
                curr_conf = logconf.loaders.ini.load(conf_file)
            elif (conf_file.endswith('.json')):
                curr_conf = logconf.loaders.json.load(conf_file)
            elif (conf_file.endswith('.xml')):
                curr_conf = logconf.loaders.xml.load(conf_file)
            elif (conf_file.endswith('.yaml')):
                curr_conf = logconf.loaders.yaml.load(conf_file)
        
            self.conf = {**curr_conf, **self.conf}

        # Load configurations from environment variables
        self.conf = {**logconf.loaders.environ.load(), **self.conf}

    def get_datefmt(self):
      """Get date format.
      If date format is not specified, default to '%d-%b-%y %H:%M:%S'.
      """
      return self.conf.get('datefmt', DEFAULT_DATEFMT)

    def get_filename(self):
      """Get log filename.
      If log filename is not specified, default to 'logconf.log'.
      """
      return self.conf.get('filename', DEFAULT_FILENAME)

    def get_filemode(self):
      """Get file mode.
      If file mode is not specified, default to 'w'.
      """
      return self.conf.get('filemode', DEFAULT_FILEMODE)

    def get_format(self):
      """Get log format.
      If log format is not specified, default to '%(asctime)s --> %(name)s - %(levelname)s - %(message)s'.
      """
      return self.conf.get('format', DEFAULT_FORMAT)

    def get_level(self):
      level = self.conf.get('level', DEFAULT_LEVEL)
      return LEVELS[level]
