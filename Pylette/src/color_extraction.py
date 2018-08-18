from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

from Pylette.src.color import Color
from Pylette.src.palette import Palette


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
        img = img.resize((64, 64))
    width, height = img.size
    arr = np.asarray(img)
    arr = np.reshape(arr, (width * height, -1))

    model = KMeans(n_clusters=palette_size, n_jobs=-1)
    model.fit_predict(arr)
    palette = np.array(model.cluster_centers_, dtype=np.int)

    colors = []
    for color in palette:
        colors.append(Color(color))

    return Palette(colors)


if __name__ == '__main__':
    palette = extract_colors('test.jpg', palette_size=10, resize=True)
    palette.display()
