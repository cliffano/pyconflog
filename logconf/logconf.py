from logconf.config import Config
import logging
import yaml

def get_logger(name, conf_files=[]):

    config = Config(conf_files=conf_files)
    logging.basicConfig(
        datefmt=config.get_datafmt(),
        filename=config.get_filename(),
        filemode=config.get_filemode(),
        format=config.get_format(),
        level=config.get_level()
    )
    logger = logging.getLogger(name)
    return logger
