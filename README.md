# Pylette

Welcome to Pylette, the easy-to-use Python library for extracting color palettes from images!

[![PyPI version](https://badge.fury.io/py/Pylette.svg)](https://badge.fury.io/py/Pylette)
[![Downloads](http://pepy.tech/badge/pylette)](http://pepy.tech/project/pylette)
[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)
![Dependabot](https://img.shields.io/badge/dependabot-enabled-025E8C?logo=dependabot&logoColor=white)

---

**Documentation**: [qtiptip.github.io/Pylette](https://qtiptip.github.io/Pylette/)

**Source code:** [qTipTip/Pylette](https://github.com/qTipTip/Pylette)

---

## What is Pylette?

Pylette is a powerful yet user-friendly library designed to help you extract color palettes from images. Whether you're
working on computer graphics, visualizations, or generative art, Pylette makes it easy to create visually appealing
color sets.

Key features:

* Extract color palettes from images
* Support for various color modes (RGB, RGBa, HSV, etc.)
* Random color selection from palettes
* Command-line interface for quick palette extraction

## Getting Started

### Installation

You can easily install Pylette using pip:

```shell
pip install Pylette
```

Or if you prefer using Poetry:

```shell
poetry add Pylette
```

### Quick Start Guide

Here's how to extract a color palette from an image and work with it in Python:

```python
from Pylette import extract_colors

palette = extract_colors(image='image.jpg', palette_size=10)
# Access colors by index
most_common_color = palette[0]
least_common_color = palette[-1]

# Get color information
print(most_common_color.rgb)
print(most_common_color.hls)
print(most_common_color.hsv)

# Display the palette, and save the image to file
palette.display(save_to_file=True)

# Save palette's color values to CSV
palette.to_csv(filename='color_palette.csv', frequency=True)

# Pick random colors
random_color = palette.random_color(N=1, mode='uniform')
random_colors = palette.random_color(N=100, mode='frequency')
```

This will give you a palette of 10 colors, sorted by frequency.
The image is automatically resized to 256x256 pixels for faster processing.
See the [documentation](https://qtiptip.github.io/Pylette) for a complete list of available methods and attributes.
