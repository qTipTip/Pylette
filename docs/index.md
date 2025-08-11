<p align="center">
  <a href="https://qtiptip.github.io/Pylette/"><img src="example_imgs/pylette_logo.jpg" alt="Pylette"></a>
</p>
<p align="center">
    <em>Welcome to Pylette, the easy-to-use Python library for extracting color palettes from images!
</em>
</p>



[![PyPI version](https://badge.fury.io/py/Pylette.svg)](https://badge.fury.io/py/Pylette)
[![Downloads](http://pepy.tech/badge/pylette)](http://pepy.tech/project/pylette)
[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)
![Dependabot](https://img.shields.io/badge/dependabot-enabled-025E8C?logo=dependabot&logoColor=white)

---

**:material-book-open-page-variant: Documentation**: [https://qtiptip.github.io/Pylette/](https://qtiptip.github.io/Pylette/)

**:fontawesome-brands-github: Source code:** [qTipTip/Pylette](https://github.com/qTipTip/Pylette)

---

## What is Pylette?

Pylette is a powerful yet user-friendly library designed to help you extract color palettes from images. Whether you're
working on computer graphics, visualizations, or generative art, Pylette makes it easy to create visually appealing
color sets.

Key features:

* Extract color palettes from images
* Support for various color modes (RGB, RGBa, HSV, etc.)
* Alpha channel support with transparency masking
* Random color selection from palettes
* Command-line interface for quick palette extraction

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

### Quick Start Guide

Here's how to extract a color palette from an image and work with it in Python:

!!! example "Extracting a Color Palette"

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
See the [reference documentation](reference.md) for a complete list of available methods and attributes.

!!! tip "Working with Transparent Images"

    For images with transparency (PNG files with alpha channels), you can use the `alpha_mask_threshold` parameter to exclude transparent or semi-transparent pixels:

    ```python
    from Pylette import extract_colors

    # Extract colors from a transparent PNG, ignoring pixels with alpha < 128
    palette = extract_colors(
        image='transparent_image.png',
        palette_size=10,
        alpha_mask_threshold=128
    )
    ```

    The `alpha_mask_threshold` parameter accepts values from 0-255, where pixels with alpha values below this threshold are excluded from color extraction.

## Command Line Tool

Pylette also comes with a handy command-line tool. Here's a quick overview of its usage:

!!! example "Command Line Usage"
    === "Options"

        ```bash

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
    === "Example"

        ```bash

        pylette --filename image.jpg \
                --mode KM \
                --n 5 \
                --sort-by luminance \
                --colorspace rgb \
                --display-colors
        ```

        For transparent images:
        ```bash
        pylette --filename transparent_image.png \
                --alpha-mask-threshold 128 \
                --n 10 \
                --display-colors
        ```



## Example Palettes

Check out these palettes extracted using Pylette! The top row corresponds to extraction using K-Means, and the bottom
row corresponds to Median-Cut extraction.
The colors are sorted by luminosity.


Original Image  | Extracted Palette
:--------------:|:-----------------:
![](https://images.unsplash.com/photo-1534535009397-1fb0a46440f1?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=0de8fee9f4e6aa3d55fef987734a0787&auto=format&fit=crop&w=1234&q=80) | ![](example_imgs/jason_leung_palette_kmeans.jpg) ![](example_imgs/jason_leung_palette_mediancut.jpg)
![](https://images.unsplash.com/photo-1534547774987-e59593542e1e?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=e8e5af1676517ac1ef8067f97a206415&auto=format&fit=crop&w=1234&q=80) | ![](example_imgs/alex_perez_palette_kmeans.jpg)  ![](example_imgs/alex_perez_palette_mediancut.jpg)
![](https://images.unsplash.com/photo-1534537841395-2e594ba9ed4a?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=34ad54d1ba5d88b42abf43219c905c78&auto=format&fit=crop&w=1234&q=80) | ![](example_imgs/josh_hild_palette_kmeans.jpg)   ![](example_imgs/josh_hild_palette_mediancut.jpg)

## How Pylette Works

Pylette uses various color quantization algorithms to extract the most representative colors from your images.
Currently, it supports:

1. K-Means clustering
2. Median-Cut algorithm

## We'd Love Your Feedback And Contributions!

Pylette is an ongoing project, and we're always looking to improve it.
If you have any suggestions, questions, or just want to share how you're using Pylette, please don't hesitate to reach
out, or make a pull request on our GitHub repository.

Happy color extracting!
