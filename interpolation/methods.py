import numpy as np
from PIL import Image


def bilinear_interpolation(img, scale_factor):
    """
    Performs bilinear image interpolation.

    Args:
        img (:mod:`PIL.image`): Original image.
        new_width (:mod:`int`): Desired width of the resized image.
        new_height (:mod:`int`): Desired height of the resized image.

    Returns:
        :mod:`PIL.Image` - resized image.
    """
    width, height = img.size

    new_width = width * scale_factor
    new_height = height * scale_factor

    resized_img = Image.new("RGB", (new_width, new_height))

    x_ratio = width / float(new_width)
    y_ratio = height / float(new_height)

    for i in range(new_height):
        for j in range(new_width):
            x = j * x_ratio
            y = i * y_ratio

            pix = [0, 0, 0]

            x1 = int(x)
            y1 = int(y)
            x2 = min(x1 + 1, width - 1)
            y2 = min(y1 + 1, height - 1)

            Q11 = img.getpixel((x1, y1))
            Q12 = img.getpixel((x1, y2))
            Q21 = img.getpixel((x2, y1))
            Q22 = img.getpixel((x2, y2))

            for ch in range(3):
                pix[ch] = (
                    int(
                        1
                        / (x2 - x1)
                        / (y2 - y1)
                        * (
                            Q11[ch] * (x2 - x) * (y2 - y)
                            + Q21[ch] * (x - x1) * (y2 - y)
                            + Q12[ch] * (x2 - x) * (y - y1)
                            + Q22[ch] * (x - x1) * (y - y1)
                        )
                    )
                    if (x2 - x1) != 0 and (y2 - y1) != 0
                    else 0
                )

            resized_img.putpixel((j, i), tuple(pix))

    return resized_img

def nearest_neighbour_interpolation(img, scale_factor):
    """
    Performs nearest neighbor image interpolation.

    Args:
        img (:mod:`PIL.Image`): Original image.
        scale_factor (:mod:`float`): Scaling factor.

    Returns:
        :mod:`PIL.Image` - resized image.
    """

    img = np.array(img)

    height, width, channels = img.shape
    new_height = int(height * scale_factor)
    new_width = int(width * scale_factor)

    resized_img = np.zeros((new_height, new_width, channels), dtype=img.dtype)

    for i in range(new_height):
        for j in range(new_width):
            old_i = int(i / scale_factor)
            old_j = int(j / scale_factor)

            old_i = min(old_i, height - 1)
            old_j = min(old_j, width - 1)

            resized_img[i, j] = img[old_i, old_j]


    return Image.fromarray(resized_img)
