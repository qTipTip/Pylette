from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

from Pylette.color import Color
from Pylette.palette import Palette


def extract_colors(image, palette_size=5, resize=True):
    """
    Extracts a set of 'palette_size' colors from the given image.
    :param image: path to Image file
    :param palette_size: number of colors to extract
    :param resize: whether to resize the image before processing, yielding faster results with lower quality
    :return: a list of the extracted colors
    """

    # open the image
    img = Image.open(image).convert('RGB')
    if resize:
        img = img.resize((256, 256))
    width, height = img.size
    arr = np.asarray(img)
    arr = np.reshape(arr, (width * height, -1))

    model = KMeans(n_clusters=palette_size)
    labels = model.fit_predict(arr)
    palette = np.array(model.cluster_centers_, dtype=np.int)
    color_count = np.bincount(labels)
    color_frequency = color_count / float(np.sum(color_count))

    colors = []
    for color, freq in zip(palette, color_frequency):
        colors.append(Color(color, freq))
    colors.sort(reverse=True)
    return Palette(colors)