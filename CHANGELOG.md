# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).




# Released

## 4.2.0 - 08/11/2025

### Added

- Added support for `PIL.Image` type in `extract_colors`.

## 4.1.0 - 4/7/2025

### Added

- Added `alpha_mask_threshold` parameter to `extract_colors()` function to support alpha channel masking for transparent images
- Colors now include alpha channel information (RGBA) and weight properties based on alpha values
- Support for filtering out transparent/semi-transparent pixels during color extraction
- Added `save()` method to `Palette` class for saving palette images without displaying them

### Changed

- Color objects now accept RGBA tuples instead of RGB tuples in constructor
- Image processing pipeline now converts all images to RGBA format internally
- Display method now uses RGBA color space for better transparency handling
- Refactored `display()` method to use the new `save()` method when `save_to_file=True`, reducing code duplication

## 4.0.1 27/01/2025

### Added

- A `ColorExtractor`-protocol that defines an interface for color extractors.
- Create a `ColorExtractorBase` abstract class that extractors can inherit from to implement the interface.

### Changed
- The implementation of `median_cut_extraction` and `k_means_extraction` is now
implemented as in terms of subclasses of the `ColorExtractorBase`

## [4.0.0] 08/10/2024

### Changed

- Overhauled the CLI to use the `typer` library for a more user-friendly experience. Note this is a breaking change for CLI users. Run `pylette --help` for more information.

## [3.0.2] 04/10/2024

### Fixed

- Fixed a bug where the CLI did not respect the `--colorspace` argument when extracting colors.
## [3.0.1] 07/07/2024

### Fixed
- Fixed a bug where the color frequencies of colors in a palette were not summing to one when using the Median Cut algorithm.

## [3.0.0] 02/07/2024

### Changed
- Changed the `image` argument to the `extract_color` function to accept:
  - A path to an image file, as a string or a pathlike.
  - An URL to an image file, as a string.
  - A byte stream of an image file, as a bytes object.
  - A numpy array of an image file, as a numpy array.
  -
## [2.3.0] 19/06/2024

- Added `image_array` to the `extract_color` function, allowing the user to specify an image as a numpy array.

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
