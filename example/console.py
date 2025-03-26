import click
from PIL import Image

from interpolation.interpolation import bilinear_interpolation


@click.command()
@click.option(
    "--file-path",
    default="example/example.jpg",
    help="Path to original image.",
)
@click.option(
    "--result-path",
    default="example/result.jpg",
    help="Path to result image.",
)
@click.option(
    "--scale-ratio",
    default=1,
    help="Scale ratio SR: new width = SR * width,\nnew height = SR * height",
)
def demo(file_path, result_path, scale_ratio):
    image = Image.open(file_path)
    width, height = image.size

    res_image = bilinear_interpolation(image, width * scale_ratio, height * scale_ratio)
    res_image.save(result_path)


if __name__ == "__main__":
    demo()
