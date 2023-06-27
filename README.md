<img align="right" src="https://raw.github.com/cliffano/pyconflog/main/avatar.jpg" alt="Avatar"/>

[![Build Status](https://github.com/cliffano/pyconflog/workflows/CI/badge.svg)](https://github.com/cliffano/pyconflog/actions?query=workflow%3ACI)
[![Vulnerabilities Status](https://snyk.io/test/github/cliffano/pyconflog/badge.svg)](https://snyk.io/test/github/cliffano/pyconflog)
[![Published Version](https://img.shields.io/pypi/v/conflog.svg)](https://pypi.python.org/pypi/conflog)
<br/>

Pyconflog
---------

Pyconflog library provides Python logging setup via environment variables and configuration files.

Installation
------------

    pip3 install pyconflog

Usage
-----

Create a configuration file, e.g. `conflog.yaml`:

    ---
    handlers: "stream,file"
    datefmt: "%Y-%m-%d %H:%M:%S"
    filename: "conflog.log"
    filemode: "w"
    format: "[SOMEAPP] [%(env)s-%(id)s] %(asctime)s %(levelname)s %(message)s"
    level: "info"
    extras:
      env: "dev"
      id: "123"
 
And then use it in your Python code:

    from conflog import Conflog

    cfl = Conflog(conf_files=['conflog.yaml'])
    logger = cfl.get_logger('somename')
    logger.debug('Some debug message')
    logger.info('Some info message')
    logger.critical('Some critical message')

It will write the log messages to stdout and file `conflog.log`:

    [SOMEAPP] [dev-123] 2023-06-07 10:49:01 INFO Some info message
    [SOMEAPP] [dev-123] 2023-06-07 10:49:52 CRITICAL Some critical message

If you specify environment variables configuration, it will overwrite the configuration files:

    import os
    from conflog import Conflog

    os.environ['CONFLOG_FORMAT'] = '[ENVAPP] [%(env)s-%(id)s] %(asctime)s %(levelname)s %(message)s'
    cfl = Conflog(conf_files=['conflog.yaml'])
    logger.debug('Some debug message')
    logger.info('Some info message')
    logger.critical('Some critical message')

It will write the log messages using the format from `CONFLOG_FORMAT` environment variable:

    [ENVAPP] [dev-123] 2023-06-07 10:49:01 INFO Some info message
    [ENVAPP] [dev-123] 2023-06-07 10:49:52 CRITICAL Some critical message

And if you specify configuration dictionary, it will overwrite everything else:

    import os
    from conflog import Conflog

    os.environ['CONFLOG_FORMAT'] = '[ENVAPP] [%(env)s-%(id)s] %(asctime)s %(levelname)s %(message)s'
    cfl = Conflog(
        conf_files=['conflog.yaml'],
        conf_dict={'format': '[DICTAPP] [%(env)s-%(id)s] %(asctime)s %(levelname)s %(message)s'})
    logger.debug('Some debug message')
    logger.info('Some info message')
    logger.critical('Some critical message')

It will write the log messages using the format from configuration dictionary:

    [DICTAPP] [dev-123] 2023-06-07 10:49:01 INFO Some info message
    [DICTAPP] [dev-123] 2023-06-07 10:49:52 CRITICAL Some critical message

Configuration
-------------

Configuration properties:

| Property | Description | Default | Example |
| -------- | ----------- | ------- | ------- |
| handlers | Comma separated list of handlers, supported values are `stream` and `file` | `stream` | `stream,file` |
| datefmt | Date format | `%d-%b-%y %H:%M:%S` | `%Y-%m-%d %H:%M:%S` |
| filename | Log file name | `conflog.log` | `someconflog.log` |
| filemode | Log file mode | `w` | `w` |
| format | Log message format | %(asctime)s --> %(name)s - %(levelname)s - %(message)s | `[SOMEAPP] [%(env)s-%(id)s] %(asctime)s %(levelname)s %(message)s` |
| level | Log level, supported values are `debug`, `info`, `warning`, `error`, `critical` | `info` | `critical` |
| extras | Extra fields to be added to log message. It can be comma separated key value pairs with equal separator, or a key value pairs map for JSON and YAML configuration files | None | `env=dev,id=123` |

Configuration files can be in YAML, JSON, XML, or INI format. Multiple files can be specified in the `conf_files` parameter when initialising `Conflog`, the configuration will be merged in the order of the files, the latter file will overwrites the former file.

Environment variables configuration overwrites configuration files' properties. And finally, configuration dictionary overwrite everything else.

### YAML

Example YAML configuration file:

    ---
    handlers: "stream,file"
    datefmt: "%Y-%m-%d %H:%M:%S"
    filename: "conflog.log"
    filemode: "w"
    format: "[SOMEAPP] [%(env)s-%(id)s] %(asctime)s %(levelname)s %(message)s"
    level: "info"
    extras:
      env: "dev"
      id: "123"

### JSON

Example JSON configuration file:

    {
      "handlers": "stream,file",
      "datefmt": "%Y-%m-%d %H:%M:%S",
      "filename": "conflog.log",
      "filemode": "w",
      "format": "[SOMEAPP] [%(env)s-%(id)s] %(asctime)s %(levelname)s %(message)s",
      "level": "info",
      "extras": {
        "env": "dev",
        "id": "123"
      }
    }

### XML

Example XML configuration file:

    <?xml version="1.0" encoding="UTF-8"?>
    <conflog>
      <handlers>stream,file</handlers>
      <datefmt>%Y-%m-%d %H:%M:%S</datefmt>
      <filename>conflog.log</filename>
      <filemode>w</filemode>
      <format>[SOMEAPP] [%(env)s-%(id)s] %(asctime)s %(levelname)s %(message)s</format>
      <level>info</level>
      <extras>env=dev,id=123</extras>
    </conflog>

### INI

Example INI configuration file:

    [conflog]
    handlers: stream,file
    datefmt: %%Y-%%m-%%d %%H:%%M:%%S
    filename: conflog.log
    filemode: w
    format: [SOMEAPP] [%%(env)s-%%(id)s] %%(asctime)s %%(levelname)s %%(message)s
    level: info
    extras: env=dev,id=123

### Environment Variables

Example configuration environment variables:

    CONFLOG_HANDLERS="stream,file"
    CONFLOG_DATEFMT="%Y-%m-%d %H:%M:%S"
    CONFLOG_FILENAME="conflog.log"
    CONFLOG_FILEMODE="w"
    CONFLOG_FORMAT="[SOMEAPP] [%(env)s-%(id)s] %(asctime)s %(levelname)s %(message)s"
    CONFLOG_LEVEL="info"
    CONFLOG_EXTRAS="env=dev,id=123"

Colophon
--------

[Developer's Guide](https://cliffano.github.io/developers_guide.html#python)

Build reports:

* [Lint report](https://cliffano.github.io/pyconflog/lint/pylint/index.html)
* [Code complexity report](https://cliffano.github.io/pyconflog/complexity/wily/index.html)
* [Unit tests report](https://cliffano.github.io/pyconflog/test/pytest/index.html)
* [Test coverage report](https://cliffano.github.io/pyconflog/coverage/coverage/index.html)
* [Integration tests report](https://cliffano.github.io/pyconflog/test-integration/pytest/index.html)
* [API Documentation](https://cliffano.github.io/pyconflog/doc/sphinx/index.html)
