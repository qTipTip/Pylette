from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

from Pylette.aux import ColorBox
from Pylette.color import Color
from Pylette.palette import Palette


def median_cut_extraction(arr, height, width, palette_size):
    """
    Extracts a color palette using the median cut algorithm.
    :param arr:
    :param height:
    :param width:
    :param palette_size:
    :return:
    """

    arr = arr.reshape((width * height, -1))
    c = [ColorBox(arr)]
    full_box_size = c[0].size

    # Each iteration, find the largest box, split it, remove original box from list of boxes, and add the two new boxes.
    while len(c) < palette_size:
        largest_c_idx = np.argmax(c)
        # add the two new boxes to the list, while removing the split box.
        c = c[:largest_c_idx] + c[largest_c_idx].split() + c[largest_c_idx + 1:]

    colors = [Color(map(int, box.average), box.size / full_box_size) for box in c]

    return colors


def extract_colors(image, palette_size=5, resize=True, mode='KM', sort_mode='luminance'):
    """
    Extracts a set of 'palette_size' colors from the given image.
    :param image: path to Image file
    :param palette_size: number of colors to extract
    :param resize: whether to resize the image before processing, yielding faster results with lower quality
    :param mode: the color quantization algorithm to use. Currently supports K-Means (KM) and Median Cut (MC)
    :param sort_mode: sort colors by luminance, or by frequency
    :return: a list of the extracted colors
    """

    # open the image
    img = Image.open(image).convert('RGB')
    if resize:
        img = img.resize((256, 256))
    width, height = img.size
    arr = np.asarray(img)

    if mode is 'KM':
        colors = k_means_extraction(arr, height, width, palette_size)
    elif mode is 'MC':
        colors = median_cut_extraction(arr, height, width, palette_size)
    else:
        raise NotImplementedError('Extraction mode not implemented')

    if sort_mode is 'luminance':
        colors.sort(key=lambda c: c.luminance, reverse=False)
    else:
        colors.sort(reverse=True)

    return Palette(colors)


def k_means_extraction(arr, height, width, palette_size):
    """
    Extracts a color palette using KMeans.
    :param arr: pixel array (height, width, 3)
    :param height: height
    :param width: width
    :param palette_size: number of colors
    :return: a palette of colors sorted by frequency
    """
    arr = np.reshape(arr, (width * height, -1))
    model = KMeans(n_clusters=palette_size)
    labels = model.fit_predict(arr)
    palette = np.array(model.cluster_centers_, dtype=np.int)
    color_count = np.bincount(labels)
    color_frequency = color_count / float(np.sum(color_count))
    colors = []
    for color, freq in zip(palette, color_frequency):
        colors.append(Color(color, freq))
    return colors
