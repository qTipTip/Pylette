<p align="center">
  <a href="https://qtiptip.github.io/Pylette/"><img src="docs/example_imgs/pylette_logo.jpg" alt="Pylette"></a>
</p>
<p align="center">
    <em>Extract color palettes from images using the command line or Python library
</em>
</p>


[![PyPI version](https://badge.fury.io/py/Pylette.svg)](https://badge.fury.io/py/Pylette)
[![Downloads](http://pepy.tech/badge/pylette)](http://pepy.tech/project/pylette)
[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)
![Dependabot](https://img.shields.io/badge/dependabot-enabled-025E8C?logo=dependabot&logoColor=white)
[![DOI](https://zenodo.org/badge/145131524.svg)](https://doi.org/10.5281/zenodo.14757252)

## What's New in v5.0

- JSON export with metadata and hex colors
- Batch processing of multiple images
- Enhanced command-line interface
- Semantic colorspace field names
- Parallel processing support

---

**Documentation**: [qtiptip.github.io/Pylette](https://qtiptip.github.io/Pylette/)

**Source code:** [qTipTip/Pylette](https://github.com/qTipTip/Pylette)

---

## What is Pylette?

Pylette helps you extract color palettes from images. Use the command-line interface for quick tasks or the Python library for more advanced workflows.

**Key Features:**
- Extract palettes from single images or batch process multiple files
- Export to JSON format with metadata and hex colors
- Support for different colorspaces (RGB, HSV, HLS)
- Handle transparent images with alpha channel masking
- Fast parallel processing for multiple images
- Rich progress display with color previews

## Getting Started

### Installation

You can easily install Pylette using pip:

```shell
pip install Pylette
```

Or if you prefer using uv:

```shell
uv add Pylette
```

## Command Line Usage

Extract palettes from images using simple commands:

```bash
# Extract 5 colors from an image
pylette image.jpg

# Process multiple images and export to JSON files
pylette *.jpg --export-json --output results/

# Extract 8 colors in HSV colorspace
pylette photo.png --n 8 --colorspace hsv --export-json --output colors.json

# Batch process with parallel processing
pylette images/*.png --export-json --output palettes/ --num-threads 4
```

### Export Formats

Export your palettes in different formats:

```bash
# Individual JSON files for each image
pylette *.jpg --export-json --output palettes/
# Creates: palette_001.json, palette_002.json, etc.

# Combined JSON file with all palettes
pylette *.jpg --export-json --output all_colors.json

# Traditional CSV output
pylette image.jpg --colorspace rgb > colors.csv
```

### Common Options

```bash
# Use different extraction algorithms
pylette image.jpg --mode MedianCut --n 6

# Handle transparent images
pylette logo.png --alpha-mask-threshold 128

# Customize output
pylette image.jpg --no-stdout --display-colors
```

## Python Library

For programmatic usage and advanced workflows:

```python
from Pylette import extract_colors

# Basic usage
palette = extract_colors(image='image.jpg', palette_size=8)

# Access color properties
for color in palette.colors:
    print(f"RGB: {color.rgb}")
    print(f"Hex: {color.hex}")
    print(f"Frequency: {color.freq:.2%}")

# Export to JSON with metadata
palette.to_json(filename='palette.json', colorspace='hsv')

# Work with different colorspaces
for color in palette.colors:
    print(f"RGB: {color.rgb}, HSV: {color.hsv}, Hex: {color.hex}")
```

The Python library provides access to all CLI functionality plus additional customization options.

## JSON Export Format

Pylette exports rich JSON data with semantic field names:

```json
{
  "colors": [
    {
      "rgb": [142, 152, 174],
      "hex": "#8E98AE",
      "frequency": 0.25
    }
  ],
  "palette_size": 5,
  "colorspace": "rgb",
  "metadata": {
    "image_source": "photo.jpg",
    "extraction_params": {
      "palette_size": 5,
      "mode": "KMeans"
    },
    "processing_stats": {
      "extraction_time": 0.234
    }
  }
}
```

Different colorspaces use appropriate field names:
- RGB: `{"rgb": [255, 128, 64], "hex": "#FF8040"}`
- HSV: `{"hsv": [0.08, 0.75, 1.0], "rgb": [255, 128, 64], "hex": "#FF8040"}`
- HLS: `{"hls": [0.08, 0.63, 0.75], "rgb": [255, 128, 64], "hex": "#FF8040"}`

## Working with Transparent Images

Handle transparency in both CLI and Python:

```bash
# CLI: Exclude pixels with alpha < 128
pylette transparent.png --alpha-mask-threshold 128
```

```python
# Python: Same functionality
from Pylette import extract_colors
palette = extract_colors('transparent.png', alpha_mask_threshold=128)
```


## Command Line Interface:

Pylette also comes with a command-line interface for quick palette extraction:

```shell
 pylette --help

 Usage: pylette [OPTIONS]

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --filename                                     PATH                   [default: None]                                                                                                                                                  │
│ --image-url                                    TEXT                   [default: None]                                                                                                                                                  │
│ --mode                                         [KM|MC]                [default: KM]                                                                                                                                                    │
│ --n                                            INTEGER                [default: 5]                                                                                                                                                     │
│ --sort-by                                      [frequency|luminance]  [default: luminance]                                                                                                                                             │
│ --stdout                --no-stdout                                   [default: stdout]                                                                                                                                                │
│ --out-filename                                 PATH                   [default: None]                                                                                                                                                  │
│ --display-colors        --no-display-colors                           [default: no-display-colors]                                                                                                                                     │
│ --colorspace                                   [rgb|hsv|hls]          [default: rgb]                                                                                                                                                   │
│ --alpha-mask-threshold                         INTEGER RANGE [0<=x<=255]  Alpha threshold for transparent image masking (0-255). Pixels with alpha below this value are excluded. [default: None]                                     │
│ --install-completion                                                  Install completion for the current shell.                                                                                                                        │
│ --show-completion                                                     Show completion for the current shell, to copy it or customize the installation.                                                                                 │
│ --help                                                                Show this message and exit.                                                                                                                                      │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
