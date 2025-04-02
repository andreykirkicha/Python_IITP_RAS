import click
from PIL import Image

from interpolation.methods import bilinear_interpolation


@click.command()
@click.option(
    "--file-path",
    default="example/example.jpg",
    help="Path to the original image.",
)
@click.option(
    "--result-path",
    default="example/result.jpg",
    help="Path to result image.",
)
@click.option(
    "--scale-ratio",
    default=1,
    help="Scale ratio :mod:`SR`: :mod:`new width` = :mod:`SR` * :mod:`width`,\n"
    ":mod:`new height` = :mod:`SR` * :mod:`height`",
)
def usage(file_path, result_path, scale_ratio):
    image = Image.open(file_path)
    width, height = image.size

    res_image = bilinear_interpolation(image, width * scale_ratio, height * scale_ratio)
    res_image.save(result_path)


if __name__ == "__main__":
    usage()
