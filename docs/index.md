# Pylette: Your Friendly Python Color Extraction Library

Welcome to Pylette, the easy-to-use Python library for extracting color palettes from images!

[![PyPI version](https://badge.fury.io/py/Pylette.svg)](https://badge.fury.io/py/Pylette)
[![Downloads](http://pepy.tech/badge/pylette)](http://pepy.tech/project/pylette)
[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)

## What is Pylette?

Pylette is a powerful yet user-friendly library designed to help you extract color palettes from images. Whether you're working on computer graphics, visualizations, or generative art, Pylette makes it easy to create visually appealing color sets.

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

## Command Line Tool

Pylette also comes with a handy command-line tool. Here's a quick overview of its usage:

!!! example "Command Line Usage"

    === "Extracting a Color Palette using the CLI"

        ```bash
        pylette --filename image.jpg --mode KM --n 5 --sort_by luminance --colorspace rgb --display-colors True
        ```

    === "Options"

        ```bash
        ╰─❯ pylette --help
        usage: pylette [-h] (--filename FILENAME | --image-url IMAGE_URL) [--mode {KM,MC}] [--n N] [--sort_by {luminance,frequency}] [--stdout STDOUT] [--colorspace {rgb,hsv,hls}] [--out_filename OUT_FILENAME]
                       [--display-colors DISPLAY_COLORS]

        options:
          -h, --help            show this help message and exit
          --filename FILENAME   path to image file (default: None)
          --image-url IMAGE_URL
                                url to the image file (default: None)
          --mode {KM,MC}        extraction_mode (KMeans/MedianCut (default: KM)
          --n N                 the number of colors to extract (default: 5)
          --sort_by {luminance,frequency}
                                sort by luminance or frequency (default: luminance)
          --stdout STDOUT       whether to display the extracted color values in the stdout (default: True)
          --colorspace {rgb,hsv,hls}
                                color space to represent colors in (default: RGB)
          --out_filename OUT_FILENAME
                                where to save the csv file (default: None)
          --display-colors DISPLAY_COLORS
                                Open a window displaying the extracted palette (default: False)

        ```

## Example Palettes

Check out these palettes extracted using Pylette! The top row corresponds to extraction using K-Means, and the bottom row corresponds to Median-Cut extraction.
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
If you have any suggestions, questions, or just want to share how you're using Pylette, please don't hesitate to reach out, or make a pull request on our GitHub repository.


Happy color extracting!
