import pytest
from PIL import Image

from interpolation.interpolation import bilinear_interpolation


@pytest.mark.parametrize("w, h, new_w, new_h", [(100, 100, 200, 200), 
                                                (100, 100, 50, 50),
                                                (100, 100, 100, 100)])
def test_new_imgsize(w, h, new_w, new_h):
    img = Image.new("RGB", (w, h), color="white")

    new_width = new_w
    new_height = new_h
    resized_img = bilinear_interpolation(img, new_width, new_height)
    print(new_width, new_height)

    assert resized_img.size == (new_width, new_height)

def test_pixel_values_in_bounds():
    img = Image.new("RGB", (2, 2), color="black")
    img.putpixel((0, 0), (255, 0, 0))  # Red
    img.putpixel((1, 0), (0, 255, 0))  # Green
    img.putpixel((0, 1), (0, 0, 255))  # Blue
    img.putpixel((1, 1), (255, 255, 255))  # White

    new_width = 4
    new_height = 4
    resized_img = bilinear_interpolation(img, new_width, new_height)

    pixel = list(resized_img.getpixel((1, 1)))

    assert all(0 <= channel <= 255 for channel in pixel)

def test_invalid_image_type():
    with pytest.raises(AttributeError):
        bilinear_interpolation("not an image", 100, 100)

def test_zero_dimensions():
    img = Image.new("RGB", (100, 100), color="white")
    with pytest.raises(ZeroDivisionError, match="division by zero"):
        bilinear_interpolation(img, 0, 0)

def test_float_scale_ratio():
    img = Image.new("RGB", (100, 100), color="white")
    with pytest.raises(TypeError):
        bilinear_interpolation(img, 100 * 1.005, 100 * 1.005)
