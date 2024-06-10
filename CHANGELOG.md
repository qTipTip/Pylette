# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

# Released

## [2.2.0] 10/06/2024

### Changed

- Added `image_bytes` to the `extract_color` function, allowing the user to specify an image as a byte stream to extract
  colors from.

## [2.1.1] 09/06/2024

### Changed

- Added `random_state` to the `KMeans` algorithm to ensure reproducibility. Two separate KMeans extractions now yield
  the same palettes. Thanks to @opeyemibami for fixing.

## [2.1.0] 07/06/2024

### Added

- Added type hints for the methods in the `Pylette` package.
- Added integration tests for color extraction. Make sure certain invariants hold for the extracted colors.

### Fixed

- Fixed the color conversion from RGB to HLS, and RGB to HSV, which was incorrect.

## [2.0.1] 14/02/2024

### Fixed

- Regression where `requests` were missing as a dependency.

## [2.0.0] 09/02/2024

### Added

- Added an `image_url` argument to the `extract_color` function, allowing the user to specify an image URL to extract
  colors from.
- Added the `--image-url` argument to the CLI, allowing the user to specify an image URL to extract colors from.

### Changed

- Changed the positional argument `filename` to an optional argument in the CLI.

## [1.0.0] 09/02/2024

### Added

### Changed

- Changed `aux.py` to `utils.py`, fixing a platform specific issue on Windows.

### Removed

- The Pylette GUI has been removed, due to problems keeping the PyQT-library
