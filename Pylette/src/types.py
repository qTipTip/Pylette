from enum import Enum


class SortMode(Enum):
    luminance = "luminance"
    frequency = "frequency"


class ExtractionMode(Enum):
    KMeans = "k_means"
    MedianCut = "median_cut"


class ColorSpace(Enum):
    RGB = "rgb"
    HSV = "hsv"
    HLS = "hls"
