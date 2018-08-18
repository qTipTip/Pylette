from setuptools import setup

setup(
    name='Pylette',
    version='0.2',
    packages=['Pylette'],
    url='https://github.com/qTipTip/Pylette',
    license='MIT',
    author='Ivar Stangeby',
    author_email='istangeby@gmail.com',
    description='A Python library for extracting color palettes from images.',
    long_description='''This Python library lets you extract a set of colors from a supplied image. The resulting 
    Palette object facilitates displaying the palette, dumping the color palette to CSV, and picking colors from the 
    palette at random.''',
    install_requires=['numpy', 'Pillow', 'scikit-learn'],
    python_requires='>=3'
)
