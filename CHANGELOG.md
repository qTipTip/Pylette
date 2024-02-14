# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## [2.0.1] 14/02/2024

### Fixed
- Regression where `requests` were missing as a dependency.

## [2.0.0] 09/02/2024

### Added

- Added an `image_url` argument to the `extract_color` function, allowing the user to specify an image URL to extract colors from.
- Added the `--image-url` argument to the CLI, allowing the user to specify an image URL to extract colors from.

### Changed

- Changed the positional argument `filename` to an optional argument in the CLI.

## [1.0.0] 09/02/2024

### Added

### Changed

- Changed `aux.py` to `utils.py`, fixing a platform specific issue on Windows.

### Removed

- The Pylette GUI has been removed, due to problems keeping the PyQT-library
