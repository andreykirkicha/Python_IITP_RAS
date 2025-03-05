import numpy as np
import matplotlib.pyplot as plt
import click
from PIL import Image
from interpolation.interpolation import bilinear_interpolation
from mpl_toolkits.mplot3d import Axes3D

@click.command()
def main():
    image = Image.open("tests/test_image.jpg")
    width, height = image.size

    res_image = bilinear_interpolation(image, width * 2, height * 2)
    res_image.save("tests/result.jpg")

if __name__ == "__main__":
    main()