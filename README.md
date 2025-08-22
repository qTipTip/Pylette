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
# Extract 5 colors from an image (shows clean table output)
pylette image.jpg

# Process multiple images and export to JSON files
pylette *.jpg --export-json --output results/

# Extract 8 colors in HSV colorspace with structured export
pylette photo.png --n 8 --colorspace hsv --export-json --output colors.json

# Batch process with parallel processing and table display
pylette images/*.png --n 6 --num-threads 4
```

**Example Output:**
```
✓ Extracted 5 colors from sunset.jpg
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Hex      ┃ RGB             ┃ Frequency┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ #FF6B35  │ (255, 107, 53)  │    28.5% │
│ #F7931E  │ (247, 147, 30)  │    23.2% │
│ #FFD23F  │ (255, 210, 63)  │    18.7% │
│ #06FFA5  │ (6, 255, 165)   │    15.4% │
│ #4ECDC4  │ (78, 205, 196)  │    14.2% │
└──────────┴─────────────────┴──────────┘
```

### Export Options

Control how your palettes are saved:

```bash
# Individual JSON files for each image
pylette *.jpg --export-json --output palettes/
# Creates: palettes/palette_001.json, palettes/palette_002.json, etc.

# Combined JSON file with all palettes
pylette *.jpg --export-json --output all_colors.json

# Export with different colorspace
pylette image.jpg --colorspace hsv --export-json --output hsv_palette.json

# Suppress table output, only export JSON
pylette *.png --export-json --output results/ --no-stdout
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

# Extract palette with rich metadata
palette = extract_colors(image='image.jpg', palette_size=8)

# Access color properties with hex support
for color in palette.colors:
    print(f"RGB: {color.rgb}")
    print(f"Hex: {color.hex}")
    print(f"HSV: {color.hsv}")
    print(f"Frequency: {color.freq:.2%}")

# Export to structured JSON
palette.to_json(filename='palette.json', colorspace='hsv')

# Access metadata
print(f"Source: {palette.image_source}")
print(f"Extraction time: {palette.processing_stats['extraction_time']:.2f}s")

# Simple export method
palette.export('my_colors', colorspace='hls', include_metadata=True)
```

### Batch Processing

For processing multiple images programmatically:

```python
from Pylette import batch_extract_colors

# Process multiple images with parallel processing
results = batch_extract_colors(
    images=['image1.jpg', 'image2.png', 'image3.jpg'],
    palette_size=8,
    max_workers=4,
    mode='KMeans'
)

# Handle results
for result in results:
    if result.success and result.palette:
        print(f"✓ {result.source}: {len(result.palette.colors)} colors")
        result.palette.export(f"{result.source}_palette")
    else:
        print(f"✗ {result.source}: {result.error}")
```

The Python library provides full programmatic access to all CLI features plus detailed metadata and customization options.

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

Different colorspaces use semantic field names:
- **RGB**: `{"rgb": [255, 128, 64], "hex": "#FF8040", "frequency": 0.25}`
- **HSV**: `{"hsv": [0.08, 0.75, 1.0], "rgb": [255, 128, 64], "hex": "#FF8040", "frequency": 0.25}`
- **HLS**: `{"hls": [0.08, 0.63, 0.75], "rgb": [255, 128, 64], "hex": "#FF8040", "frequency": 0.25}`

### Interactive Table Output

When run without `--export-json`, Pylette displays a clean table:

```
✓ Extracted 5 colors from photo.jpg
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Hex      ┃ RGB             ┃ Frequency┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ #FF8040  │ (255, 128, 64)  │    25.2% │
│ #4080FF  │ (64, 128, 255)  │    30.1% │
└──────────┴─────────────────┴──────────┘
```

The table automatically adapts to show the chosen colorspace (RGB, HSV, or HLS).

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

## Why Choose Pylette?

- **Clean, Visual Output**: No more raw CSV dumps - see your colors in beautiful tables
- **Rich Metadata**: Every palette includes extraction details, timing, and image info
- **Flexible Export**: JSON format with semantic field names for easy parsing
- **Batch Ready**: Process hundreds of images with parallel processing and progress bars
- **Developer Friendly**: Comprehensive Python API with full type hints
- **Modern CLI**: Intuitive commands that guide you toward the right options


## CLI Reference

For complete usage information:

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
