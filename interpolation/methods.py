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
            x = j / scale_factor
            y = i / scale_factor

            x1 = int(np.floor(x))
            y1 = int(np.floor(y))
            x2 = min(x1 + 1, width - 1)
            y2 = min(y1 + 1, height - 1)

            dx = x - x1
            dy = y - y1

            for ch in range(channels):
                value = (
                    img_array[y1, x1, ch] * (1 - dx) * (1 - dy)
                    + img_array[y1, x2, ch] * dx * (1 - dy)
                    + img_array[y2, x1, ch] * (1 - dx) * dy
                    + img_array[y2, x2, ch] * dx * dy
                )

                resized_img[i, j, ch] = np.clip(value, 0, 255)

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


def cubic_kernel(x: float) -> float:
    x = abs(x)
    if x <= 1:
        return 1.5 * x**3 - 2.5 * x**2 + 1
    elif 1 < x < 2:
        return -0.5 * x**3 + 2.5 * x**2 - 4 * x + 2
    else:
        return 0


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

    for i in range(new_height):
        for j in range(new_width):
            x = j / scale_factor
            y = i / scale_factor

            x_int = int(np.floor(x))
            y_int = int(np.floor(y))

            dx = x - x_int
            dy = y - y_int

            pixel_value = np.zeros(channels)
            for m in range(-1, 3):
                for n in range(-1, 3):
                    x_idx = min(max(x_int + n, 0), width - 1)
                    y_idx = min(max(y_int + m, 0), height - 1)

                    weight_x = cubic_kernel(n - dx)
                    weight_y = cubic_kernel(m - dy)

                    for ch in range(channels):
                        pixel_value[ch] += (
                            img_array[y_idx, x_idx, ch] * weight_x * weight_y
                        )

            for ch in range(channels):
                resized_img[i, j, ch] = np.clip(pixel_value[ch], 0, 255)

    return Image.fromarray(resized_img.astype(np.uint8))
