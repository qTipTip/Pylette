from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

from Pylette.src.color import Color


def extract_colors(image, palette_size=5, resize=True):
    """
    Extracts a set of 'palette_size' colors from the given image.
    :param palette_size: number of colors to extract
    :return: a list of the extracted colors
    // https://stackoverflow.com/a/18801274
    """

    # open the image
    img = Image.open(image).convert('RGB')
    if resize:
        img = img.resize((32, 32))
    width, height = img.size
    depth = 3
    arr = np.asarray(img)
    arr = np.reshape(arr, (width * height, -1))

    model = KMeans(n_clusters=palette_size)
    labels = model.fit_predict(arr)
    palette = np.array(model.cluster_centers_, dtype=np.int)

    colors = []
    for color in palette:
        colors.append(Color(color, 1))

    return colors

if __name__ == '__main__':
    palette = extract_colors('test.jpg', palette_size=10, resize=True)

    for color in palette:
        color.display()