import numpy as np
import pytest
from PIL import Image

from interpolation import methods

bilinear_interpolation = methods.bilinear_interpolation
nearest_neighbour_interpolation = methods.nearest_neighbour_interpolation
bicubic_interpolation = methods.bicubic_interpolation


@pytest.mark.parametrize(
    "interpolation, w, h, scale_factor",
    [
        (bilinear_interpolation, 100, 100, 2),
        (bilinear_interpolation, 100, 100, 0.5),
        (bilinear_interpolation, 100, 100, 1),
        (bilinear_interpolation, 100, 100, 1.005),
        (nearest_neighbour_interpolation, 100, 100, 2),
        (nearest_neighbour_interpolation, 100, 100, 0.5),
        (nearest_neighbour_interpolation, 100, 100, 1),
        (nearest_neighbour_interpolation, 100, 100, 1.005),
        (bicubic_interpolation, 100, 100, 2),
        (bicubic_interpolation, 100, 100, 0.5),
        (bicubic_interpolation, 100, 100, 1),
        (bicubic_interpolation, 100, 100, 1.005),
    ],
)
def test_new_imgsize(interpolation, w, h, scale_factor):
    img = Image.new("RGB", (w, h), color="white")

    new_width = int(w * scale_factor)
    new_height = int(h * scale_factor)
    resized_img = interpolation(img, scale_factor)

    assert resized_img.size == (new_width, new_height)


@pytest.mark.parametrize(
    "interpolation",
    [bilinear_interpolation, nearest_neighbour_interpolation, bicubic_interpolation],
)
def test_pixel_values_in_bounds(interpolation):
    img = Image.new("RGB", (2, 2), color="black")
    img.putpixel((0, 0), (255, 0, 0))  # Red
    img.putpixel((1, 0), (0, 255, 0))  # Green
    img.putpixel((0, 1), (0, 0, 255))  # Blue
    img.putpixel((1, 1), (255, 255, 255))  # White

    resized_img = interpolation(img, 2)

    pixel = list(resized_img.getpixel((1, 1)))

    assert all(0 <= channel <= 255 for channel in pixel)


@pytest.mark.parametrize(
    "interpolation",
    [bilinear_interpolation, nearest_neighbour_interpolation, bicubic_interpolation],
)
def test_close_pixel_values(interpolation):
    img = Image.new("RGB", (2, 2), color="black")
    img.putpixel((0, 0), (10, 20, 30))
    img.putpixel((0, 1), (40, 50, 60))
    img.putpixel((1, 0), (70, 80, 90))
    img.putpixel((1, 1), (100, 110, 120))

    resized_img = interpolation(img, 2)
    result = np.array(resized_img)

    assert np.allclose(result[0, 0], [10, 20, 30], atol=10)
    assert np.allclose(result[-1, -1], [100, 110, 120], atol=10)


@pytest.mark.parametrize(
    "interpolation",
    [bilinear_interpolation, nearest_neighbour_interpolation, bicubic_interpolation],
)
def test_invalid_image_type(interpolation):
    with pytest.raises(ValueError):
        interpolation("not an image", 1)


@pytest.mark.parametrize(
    "interpolation",
    [bilinear_interpolation, nearest_neighbour_interpolation, bicubic_interpolation],
)
def test_zero_scale_factor(interpolation):
    img = Image.new("RGB", (100, 100), color="white")
    with pytest.raises(ValueError, match="Scale factor must be greater than zero"):
        interpolation(img, 0)


@pytest.mark.parametrize(
    "interpolation",
    [bilinear_interpolation, nearest_neighbour_interpolation, bicubic_interpolation],
)
def test_negative_scale_factor(interpolation):
    img = Image.new("RGB", (100, 100), color="white")
    with pytest.raises(ValueError, match="Scale factor must be greater than zero"):
        interpolation(img, -0.5)
