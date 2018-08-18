from PIL import Image
import numpy as np


class Palette():

    def __init__(self, colors):
        """
        Initializes a color palette with a list of Color objects.
        :param colors: a list of Color-objects
        """

        self.colors = colors
        self.frequencies = [c.freq for c in colors]
        self.number_of_colors = len(colors)

    def display(self, w=50, h=50, save_to_file=False):
        img = Image.new('RGB', size=(w * self.number_of_colors, h))
        arr = np.asarray(img).copy()
        for i in range(self.number_of_colors):
            c = self.colors[i]
            arr[:, i * h:(i + 1) * h, :] = c.rgb
        img = Image.fromarray(arr, 'RGB')
        img.show()

        if save_to_file:
            img.save('color_palette.jpg')

    def __getitem__(self, item):
        return self.colors[item]

    def __len__(self):
        return self.number_of_colors

    def to_csv(self, filename='palette.csv', frequency=True):
        """
        Dumps the palette to a comma separated text file
        :param filename: file to dump to
        :param frequency: whether to dump the corresponding frequency of each color
        """
        with open(filename, 'w') as palette_file:
            for color in self.colors:
                palette_file.write(','.join(map(str, color.rgb)))
                if frequency:
                    palette_file.write(',{}'.format(color.freq))
                palette_file.write('\n')

    def random_color(self, N, mode='frequency'):
        """
        Returns N random colors from the palette, either using the frequency of each color, or
        choosing uniformly.
        :param mode: frequency/uniform
        :return: a color from the Palette
        """

        if mode is 'frequency':
            pdf = self.frequencies
        elif mode is 'uniform':
            pdf = None

        return np.random.choice(self.colors, size=N, p=pdf)