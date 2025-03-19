from PIL import Image


def create_sample_image(width, height, img_color):
    return Image.new("RGB", (width, height), color=img_color)
