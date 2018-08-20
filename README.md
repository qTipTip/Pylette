# Pylette [WIP]

A color palette extractor written in Python using KMeans clustering.

## Motivation

Working with computer graphics and visualizations, one often needs a way of specifying a set of colors
with a certain visual appeal. Such a set of colors is often called a *color palette*. The aim of this
library is to easily extract a set of colors from a supplied image, with support for the various color modes (RGB, RGBa, HSV, etc).
Dabbling in generative art, the need often arises for being able to pick colors at random from a palette. 
Pylette supports this, both picking colors uniformly, but also using the color frequency from the original image as probabilities. 



#### Other color palette related Python-libraries:
1. [Color Thief](https://github.com/fengsp/color-thief-py): Extraction of color palettes using the median cut algorithm. 
2. [Palettable](https://pypi.org/project/palettable/): Generation of matplotlib compatible color schemes
3. [Colorgram](https://github.com/obskyr/colorgram.py): Extraction of colors from images (similar to the intended use of this library),
however, I was unable to install this.

## Installation

Pylette is available in the python package index (PyPi), and can be installed using `pip`:

```shell
pip install Pylette
```

## Basic usage

A `Palette` object is created by calling the `extract_colors` function.

```python
from Pylette import extract_colors

palette = extract_colors('image.jpg', palette_size=10, resize=True)
```

This yields a palette of ten colors, and the `resize` flag tells Pylette to resize the image to a more manageable size before
beginning color extraction. This significantly speeds up the extraction, but reduces the faithfulness of the color palette.
The palette object supports indexing and iteration, and the colors are sorted from highest to lowest frequency by default.
 E.g, the following snippet will fetch the most common, and least common
color in the picture:
```python
most_common_color = palette[0]
least_common_color = palette[-1]
three_most_common_colors = palette[:3]
```
As seen, slicing is also supported.

The Palette object contains a list of Color objects, which contains a representation of the color in various color modes, with RGB being the default. Accessing the color attributes is easy:

```python
color = palette[0]

print(color.rgb)
print(color.hls)
print(color.hsv)
```

To display the extracted color palette, simply call the `display`-method, which optionally takes a flag for saving the palette to an image file.
The palette can be dumped to a CSV-file as well, where each row represents the RGB values and the corresponding color frequency (optional).
```python
palette.display(save_to_file=False)
palette.to_csv(filename='color_palette.csv', frequency=True)
```

In order to pick colors from the palette at random, Pylette offers the `random_color`-method, which supports both drawing
uniformly, and from the original color distribution, given by the frequencies of the extracted colors:

```python
random_color = palette.random_color(N=1, mode='uniform')
random_colors = palette.random_color(N=100, mode='frequency')
```

## Example Palettes

Original Image  | Extracted Palette
:--------------:|:-----------------:
<img src="https://images.unsplash.com/photo-1534535009397-1fb0a46440f1?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=0de8fee9f4e6aa3d55fef987734a0787&auto=format&fit=crop&w=1234&q=80" width=200 height=200> | ![](example_imgs/jason_leung_palette_kmeans.jpg) ![](example_imgs/jason_leung_palette_mediancut.jpg) 
<img src="https://images.unsplash.com/photo-1534547774987-e59593542e1e?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=e8e5af1676517ac1ef8067f97a206415&auto=format&fit=crop&w=1234&q=80" width=200 height=200> | ![](example_imgs/alex_perez_palette_kmeans.jpg)  ![](example_imgs/alex_perez_palette_mediancut.jpg)
<img src="https://images.unsplash.com/photo-1534537841395-2e594ba9ed4a?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=34ad54d1ba5d88b42abf43219c905c78&auto=format&fit=crop&w=1234&q=80" width=200 height=200> | ![](example_imgs/josh_hild_palette_kmeans.jpg)   ![](example_imgs/josh_hild_palette_mediancut.jpg)

## Under the hood

Currently, Pylette uses KMeans for the color quantization. There are plans for implementing other color quantization schemes, like:

1. Median-cut
2. Octree
3. Modified minmax

The article [*Improving the Performance of K-Means for Color Quantization*](https://arxiv.org/pdf/1101.0395.pdf) gives a 
nice overview of available methods.

## Feedback
Any feedback and suggestions is much appreciated. 
This is very much a work in progress. 
