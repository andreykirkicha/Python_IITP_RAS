import click
from PIL import Image

from interpolation import methods

bilinear_interpolation = methods.bilinear_interpolation
nearest_neighbour_interpolation = methods.nearest_neighbour_interpolation
bicubic_interpolation = methods.bicubic_interpolation


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
    "--method",
    default="bilinear",
    help="Interpolation method: bilinear, nearest_neighbour, bicubic",
)
@click.option(
    "--scale-factor",
    default=1,
    help="Scale factor :mod:`SF`: :mod:`new width` = :mod:`SF` * :mod:`width`,\n"
    ":mod:`new height` = :mod:`SF` * :mod:`height`",
)
def usage(file_path, result_path, method, scale_factor):
    image = Image.open(file_path)

    if method == "bilinear":
        interpolation = bilinear_interpolation
    elif method == "nearest_neighbour":
        interpolation = nearest_neighbour_interpolation
    elif method == "bicubic":
        interpolation = bicubic_interpolation

    res_image = interpolation(image, scale_factor)
    res_image.save(result_path)


if __name__ == "__main__":
    usage()
