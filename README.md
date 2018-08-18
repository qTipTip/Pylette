# Pylette [WIP]

A color palette extractor written in Python.

## Motivation

Working with computer graphics and visualizations, one often needs a way of specifying a set of colors
with a certain visual appeal. Such a set of colors is often called a *color palette*. The aim of this
library is to easily extract a set of colors from a supplied image, with support for the various color modes (RGB, RGBa, HSV, etc).
Dabbling in generative art, the need often arises for being able to pick colors at random from a palette. 
Pylette supports this, 
both picking colors uniformly, but also using the color frequency from the original image as probabilities. 


#### Other color palette related Python-libraries:

1. [Palettable](https://pypi.org/project/palettable/): Generation of matplotlib compatible color schemes
2. [Colorgram](https://github.com/obskyr/colorgram.py): Extraction of colors from images (similar to the intended use of this library),
however, I was unable to install this.

## Installation


