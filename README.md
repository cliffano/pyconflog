<img align="right" src="https://raw.github.com/cliffano/pylogconf/main/avatar.jpg" alt="Avatar"/>

[![Build Status](https://github.com/cliffano/pylogconf/workflows/CI/badge.svg)](https://github.com/cliffano/pylogconf/actions?query=workflow%3ACI)
[![Vulnerabilities Status](https://snyk.io/test/github/cliffano/pylogconf/badge.svg)](https://snyk.io/test/github/cliffano/pylogconf)
[![Published Version](https://img.shields.io/pypi/v/pylogconf.svg)](https://pypi.python.org/pypi/pylogconf)
<br/>

Pylogconf
---------

Pylogconf library provides Python logging setup via environment variables and configuration files.

Installation
------------

    pip3 install pylogconf

Usage
-----

Create a configuration file, e.g. `logconf.yaml`:

    ---
    handlers: "stream,file"
    datefmt: "%Y-%m-%d %H:%M:%S"
    filename: "logconf.log"
    filemode: "w"
    format: "[SOMEAPP] [%(env)s-%(id)s] %(asctime)s %(levelname)s %(message)s"
    level: "info"
    extras:
      env: "dev"
      id: "123"
 
And then use it in your Python code:

    from logconf import Logconf

    lc = logconf.Logconf(conf_files=['logconf.yaml'])
    logger = lc.get_logger('somename')
    logger.debug('Some debug message')
    logger.info('Some info message')
    logger.critical('Some critical message')

It will write the log messages to stdout and file `logconf.log`:

    [SOMEAPP] [dev-123] 2023-06-07 10:49:01 INFO Some info message
    [SOMEAPP] [dev-123] 2023-06-07 10:49:52 CRITICAL Some critical message

Configuration
-------------

Configuration properties:

| Property | Description | Default | Example |
| -------- | ----------- | ------- | ------- |
| handlers | Comma separated list of handlers, supported values are `stream` and `file` | `stream` | `stream,file` |
| datefmt | Date format | `%d-%b-%y %H:%M:%S` | `%Y-%m-%d %H:%M:%S` |
| filename | Log file name | `logconf.log` | `somelogconf.log` |
| filemode | Log file mode | `w` | `w` |
| format | Log message format | %(asctime)s --> %(name)s - %(levelname)s - %(message)s | `[SOMEAPP] [%(env)s-%(id)s] %(asctime)s %(levelname)s %(message)s` |
| level | Log level, supported values are `debug`, `info`, `warning`, `error`, `critical` | `info` | `critical` |
| extras | Extra fields to be added to log message. It can be comma separated key value pairs with equal separator, or a key value pairs map for JSON and YAML configuration files | None | `env=dev,id=123` |

Configuration files can be in YAML, JSON, XML, or INI format. Multiple files can be specified in the `conf_files` parameter when initialising `Logconf`, the configuration will be merged in the order of the files, the latter file will override the former file, and environment variables override configuration files' properties.

### YAML

Example YAML configuration file:

    ---
    handlers: "stream,file"
    datefmt: "%Y-%m-%d %H:%M:%S"
    filename: "logconf.log"
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
      "filename": "logconf.log",
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
    <logconf>
      <handlers>stream,file</handlers>
      <datefmt>%Y-%m-%d %H:%M:%S</datefmt>
      <filename>logconf.log</filename>
      <filemode>w</filemode>
      <format>[SOMEAPP] [%(env)s-%(id)s] %(asctime)s %(levelname)s %(message)s</format>
      <level>info</level>
      <extras>env=dev,id=123</extras>
    </logconf>

### INI

Example INI configuration file:

    [logconf]
    handlers: stream,file
    datefmt: %%Y-%%m-%%d %%H:%%M:%%S
    filename: logconf.log
    filemode: w
    format: [SOMEAPP] [%%(env)s-%%(id)s] %%(asctime)s %%(levelname)s %%(message)s
    level: info
    extras: env=dev,id=123

### Environment Variables

Example configuration environment variables:

    LOGCONF_HANDLERS="stream,file"
    LOGCONF_DATEFMT="%Y-%m-%d %H:%M:%S"
    LOGCONF_FILENAME="logconf.log"
    LOGCONF_FILEMODE="w"
    LOGCONF_FORMAT="[SOMEAPP] [%(env)s-%(id)s] %(asctime)s %(levelname)s %(message)s"
    LOGCONF_LEVEL="info"
    LOGCONF_EXTRAS="env=dev,id=123"

Colophon
--------

[Developer's Guide](https://cliffano.github.io/developers_guide.html#nodejs)

Build reports:

* [Lint report](https://cliffano.github.io/pylogconf/lint/pylint/index.html)
* [Code complexity report](https://cliffano.github.io/pylogconf/complexity/wily/index.html)
* [Unit tests report](https://cliffano.github.io/pylogconf/test/pytest/index.html)
* [Test coverage report](https://cliffano.github.io/pylogconf/coverage/coverage/index.html)
* [Integration tests report](https://cliffano.github.io/pylogconf/test-integration/pytest/index.html)
* [API Documentation](https://cliffano.github.io/pylogconf/doc/sphinx/index.html)
