import numpy as np
from PIL import Image


def bilinear_interpolation(img, scale_factor):
    """
    Performs bilinear image interpolation.

    Args:
        img (:mod:`PIL.Image`): Original image.
        scale_factor (:mod:`float`): Scaling factor.

    Returns:
        :mod:`PIL.Image` - resized image.
    """

    img_array = np.array(img).astype(np.float32)

    height, width, channels = img_array.shape
    new_height = int(height * scale_factor)
    new_width = int(width * scale_factor)

    resized_img = np.zeros((new_height, new_width, channels), dtype=img_array.dtype)

    for i in range(new_height):
        for j in range(new_width):
            x = int(j / scale_factor)
            y = int(i / scale_factor)

            x1 = min(x, width - 1)
            y1 = min(y, height - 1)

            x2 = min(x1 + 1, width - 1)
            y2 = min(y1 + 1, height - 1)

            for ch in range(channels):
                resized_img[i, j, ch] = (
                    int(
                        1
                        / (x2 - x1)
                        / (y2 - y1)
                        * (
                            img_array[y1, x1, ch] * (x2 - x) * (y2 - y)
                            + img_array[y1, x2, ch] * (x - x1) * (y2 - y)
                            + img_array[y2, x1, ch] * (x2 - x) * (y - y1)
                            + img_array[y2, x2, ch] * (x - x1) * (y - y1)
                        )
                    )
                    if (x2 - x1) != 0 and (y2 - y1) != 0
                    else 0
                )

    return Image.fromarray(resized_img.astype(np.uint8))


def nearest_neighbour_interpolation(img, scale_factor):
    """
    Performs nearest neighbor image interpolation.

    Args:
        img (:mod:`PIL.Image`): Original image.
        scale_factor (:mod:`float`): Scaling factor.

    Returns:
        :mod:`PIL.Image` - resized image.
    """

    img_array = np.array(img)

    height, width, channels = img_array.shape
    new_height = int(height * scale_factor)
    new_width = int(width * scale_factor)

    resized_img = np.zeros((new_height, new_width, channels), dtype=img_array.dtype)

    for i in range(new_height):
        for j in range(new_width):
            old_i = int(i / scale_factor)
            old_j = int(j / scale_factor)

            old_i = min(old_i, height - 1)
            old_j = min(old_j, width - 1)

            resized_img[i, j] = img_array[old_i, old_j]

    return Image.fromarray(resized_img)
