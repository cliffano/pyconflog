# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added
- Add Python 3.12 support

## 1.5.1 - 2023-08-09
### Fixed
- Fix PyYAML 6.0.1 upgrade missed out from setup.py

## 1.5.0 - 2023-08-09
### Changed
- Allow case-insensitive level configuration

### Fixed
- Fix installation error with Cython 3.0.0a10 via PyYAML 6.0.1 upgrade

## 1.4.0 - 2023-06-27
### Added
- Add function signature type hints
- Add configuration dictionary support

## 1.3.0 - 2023-06-14
### Added
- Add adapter-level log level setting

## 1.2.0 - 2023-06-14
### Added
- Add handler-level log level setting

## 1.1.0 - 2023-06-14
### Added
- Add Conflog.get_config_properties method

### Fixed
- Fix missing PyYAML dependency

## 1.0.1 - 2023-06-08
### Fixed
- Fix publish workflow, shift commands to Makefile

## 1.0.0 - 2023-06-08
### Added
- Add single conf file string arg support for Conflog constructor

### Fixed
- Fix missing dist/ folder prior to publishing to Pypi

## 0.10.0 - 2023-06-07
### Added
- Initial version
