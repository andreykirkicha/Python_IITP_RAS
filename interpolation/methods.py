import numpy as np
from PIL import Image


def bilinear_interpolation(img: Image, scale_factor: float) -> Image:
    """
    Performs bilinear image interpolation.

    Args:
        img (:class:`PIL.Image.Image`): Original image.
        scale_factor (:obj:`float`): Scaling factor.

    Returns:
        :class:`PIL.Image.Image` - resized image.
    """

    if scale_factor <= 0:
        raise ValueError("Scale factor must be greater than zero")

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


def nearest_neighbour_interpolation(img: Image, scale_factor: float) -> Image:
    """
    Performs nearest neighbor image interpolation.

    Args:
        img (:class:`PIL.Image.Image`): Original image.
        scale_factor (:obj:`float`): Scaling factor.

    Returns:
        :class:`PIL.Image.Image` - resized image.
    """

    if scale_factor <= 0:
        raise ValueError("Scale factor must be greater than zero")

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


def bicubic_interpolation(img: Image, scale_factor: float) -> Image:
    """
    Performs bicubic image interpolation.

    Args:
        img (:class:`PIL.Image.Image`): Original image.
        scale_factor (:obj:`float`): Scaling factor.

    Returns:
        :class:`PIL.Image.Image` - resized image.
    """

    if scale_factor <= 0:
        raise ValueError("Scale factor must be greater than zero")

    img_array = np.array(img).astype(np.float32)

    height, width, channels = img_array.shape
    new_height = int(height * scale_factor)
    new_width = int(width * scale_factor)

    resized_img = np.zeros((new_height, new_width, channels), dtype=img_array.dtype)

    def cubic_kernel(x):
        x = np.abs(x)
        if x <= 1:
            return 1 - 2 * x**2 + x**3
        elif x < 2:
            return 4 - 8 * x + 5 * x**2 - x**3
        else:
            return 0

    for i in range(new_height):
        for j in range(new_width):
            x = j / scale_factor
            y = i / scale_factor

            x1 = int(np.floor(x))
            y1 = int(np.floor(y))

            for ch in range(channels):
                a = np.zeros((4, 4))
                for m in range(-1, 3):
                    for n in range(-1, 3):
                        x_coord = min(max(x1 + n, 0), width - 1)
                        y_coord = min(max(y1 + m, 0), height - 1)
                        a[m + 1, n + 1] = img_array[y_coord, x_coord, ch]

                coeffs = np.zeros(16)
                for m in range(4):
                    for n in range(4):
                        coeffs[m * 4 + n] = a[m, n]

                sx = x - x1
                sy = y - y1

                bx = np.array(
                    [
                        cubic_kernel(sx + 1),
                        cubic_kernel(sx),
                        cubic_kernel(1 - sx),
                        cubic_kernel(2 - sx),
                    ]
                )
                by = np.array(
                    [
                        cubic_kernel(sy + 1),
                        cubic_kernel(sy),
                        cubic_kernel(1 - sy),
                        cubic_kernel(2 - sy),
                    ]
                )

                resized_img[i, j, ch] = np.clip(np.dot(by, np.dot(a, bx)), 0, 255)

    return Image.fromarray(resized_img.astype(np.uint8))
