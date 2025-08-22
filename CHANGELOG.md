# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


# Released

## 5.1.0 - 22/08/2025

### Fixed
- Added OpenCV as required dependency

### Added
- Expose the `types`-module to the user, so they can import Pylette types from `Pylette.types`.

## 5.0.1 - 22/08/2025

### Changed
- **to_json() API**: Removed `stdout` parameter from `to_json()` method - method now only returns JSON data without printing

## 5.0.0 - 22/08/2025

### Added
- **JSON Export**: New `to_json()` method on `Palette` class for exporting palettes to JSON format
- **Enhanced CLI Export**:
  - `--export-json` flag for JSON output
  - `--output` parameter supporting both individual files and combined export
- **Batch Processing**: Process multiple images in a single CLI command with parallel processing
- **Color Hex Representation**: `hex` property on `Color` class providing `#RRGGBB` format
- **Palette Metadata**: Metadata including image source, extraction parameters, and processing statistics
- **Enhanced Progress Display**: CLI shows recently extracted palettes with color previews
- **Rich Table Output**: Clean, colorized table display for CLI showing hex values, RGB/HSV/HLS, and frequencies

### Changed
- **CLI Interface**: Removed `--filename` and `--image-url` parameters in favor of positional image arguments
- **Batch Processing**: CLI now processes multiple image sources by default

### Removed
- **CSV Export**: Removed `to_csv()` method from `Palette` class - use JSON export instead

### Breaking Changes
- CLI parameter changes: `--filename` and `--image-url` removed
- `Palette.to_csv()` method removed


## 4.4.0 - 20/08/2025

### Changed

- Raise a ValueError if there are no pixels left after alpha channel masking.

### Fixed

- Local imports improve startup speed for CLI based usage, especially when not
requiring K Means extraction.

## 4.3.0 - 11/08/2025

### Added

• Added `types.py` file containing custom type definitions

### Changed

• Replaced mypy with pyright for type checking
• Updated and improved type annotations
• Replaced pre-commit hooks with local tools

### Fixed

• Fixed an issue with np.argmax and ColorBox not implementing the __array__ protocol, improving NumPy compatibility

## 4.2.0 - 11/08/2025

### Added

- Added support for `PIL.Image` type in `extract_colors`.

## 4.1.0 - 04/07/2025

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
