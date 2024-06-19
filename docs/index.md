# Pylette: The friendly Python color extraction library

Pylette is a Python library that allows you to extract colors from images.
It is designed to be simple to use, and easy to integrate into your projects.

## Installation

You can install Pylette using pip:

```bash
pip install pylette
```

## Usage

Pylette offers support for various image sources, such as URLs, files, byte streams, and numpy arrays.
With simplicity in mind, Pylette provides a single function to extract colors from an image:

```python
from Pylette import extract_colors

palette = extract_colors(image="path/to/image.jpg", palette_size=10)
```

The extracted colors are returned as a `Palette`-object, which is a collection of `Color`-objects.
Each `Color`-object contains the RGB, HLS, and HSV values of the color, along with the frequency of the color in the
image.

A `Palette`-object can used to sample colors, get the most/least dominant colors, or to visualize the colors in the palette.

```python
from Pylette import extract_colors

palette = extract_colors(image="path/to/image.jpg", palette_size=10)
sampled_colors = palette.random_color(N=10, mode="frequency")  # Sample 10 colors from the palette based on color distribution

most_dominant_color = palette[0]
least_dominant_color = palette[-1]

palette.display()  # Display the colors in the palette
```

## Examples

A selection of example palettes. Each palette is sorted by luminance (percieved brightness). The top row corresponds to extraction using K-Means, and the bottom row corresponds to Median-Cut extraction.

Original Image  | Extracted Palette
:--------------:|:-----------------:
<img src="https://images.unsplash.com/photo-1534535009397-1fb0a46440f1?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=0de8fee9f4e6aa3d55fef987734a0787&auto=format&fit=crop&w=1234&q=80" width=200 height=200> | ![](example_imgs/jason_leung_palette_kmeans.jpg) ![](example_imgs/jason_leung_palette_mediancut.jpg)
<img src="https://images.unsplash.com/photo-1534547774987-e59593542e1e?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=e8e5af1676517ac1ef8067f97a206415&auto=format&fit=crop&w=1234&q=80" width=200 height=200> | ![](example_imgs/alex_perez_palette_kmeans.jpg)  ![](example_imgs/alex_perez_palette_mediancut.jpg)
<img src="https://images.unsplash.com/photo-1534537841395-2e594ba9ed4a?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=34ad54d1ba5d88b42abf43219c905c78&auto=format&fit=crop&w=1234&q=80" width=200 height=200> | ![](example_imgs/josh_hild_palette_kmeans.jpg)   ![](example_imgs/josh_hild_palette_mediancut.jpg)
