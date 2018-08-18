from PIL import Image
import numpy as np


class Palette():

    def __init__(self, colors):
        """
        Initializes a color palette with a list of Color objects.
        :param colors: a list of Color-objects
        """

        self.colors = colors
        self.number_of_colors = len(colors)

    def display(self, w=50, h=50):
        img = Image.new('RGB', size=(w * self.number_of_colors, h))
        arr = np.asarray(img).copy()
        for i in range(self.number_of_colors):
            c = self.colors[i]
            arr[:, i * h:(i + 1) * h, :] = c.rgb
        img = Image.fromarray(arr, 'RGB')
        img.show()

    def __getitem__(self, item):
        return self.colors[item]

    def __len(self):
        return self.number_of_colors

