"""
Utilities for processing and adding watermarks to images

"""
from enum import Enum
from math import sqrt

from PIL import Image


class Corner(Enum):
    UPPER_LEFT = 'upper left'
    UPPER_RIGHT = 'upper right'
    LOWER_LEFT = 'lower left'
    LOWER_RIGHT = 'lower right'


def average_colors(image: Image) -> tuple[int, int, int]:
    """
    Average colors of an image

    :param image: Image
    :return: tuple (red, green, blue)
    """
    red, green, blue = 0, 0, 0
    pixel_count = image.width * image.height

    for x in range(image.width):
        for y in range(image.height):
            r, g, b = image.getpixel((x, y))
            red += r
            green += g
            blue += b

    return red // pixel_count, green // pixel_count, blue // pixel_count


def colors_stdev(image: Image) -> tuple[float, float, float]:
    """
    Standard deviations of RGB colors in an image

    :param image: image to process
    :return: standard deviations (red, green, blue)
    """

    avg_red, avg_green, avg_blue = average_colors(image)
    pixel_count = image.width * image.height
    red, green, blue = 0, 0, 0

    for x in range(image.width):
        for y in range(image.height):
            r, g, b = image.getpixel((x, y))
            red += r ** 2
            green += g ** 2
            blue += b ** 2

    std_red = sqrt((red / pixel_count) - avg_red ** 2)
    std_green = sqrt((green / pixel_count) - avg_green ** 2)
    std_blue = sqrt((blue / pixel_count) - avg_blue ** 2)

    return std_red, std_green, std_blue


def cut_corner(image: Image, corner: Corner, width_proportion: float, height_proportion: float) -> Image:
    """
    Returns a corner of the image of specified proportions

    :param image: Image to cut out from
    :param corner: Corner object
    :param width_proportion: float [0.0, 1.0]
    :param height_proportion: float [0.0, 1.0]
    :return: Image object representing the corner
    """
    width = image.width * width_proportion
    height = image.height * height_proportion

    x_start, x_end, y_start, y_end = None, None, None, None

    match corner:
        case Corner.UPPER_LEFT:
            x_start = 0
            x_end = width
            y_start = 0
            y_end = height
        case Corner.UPPER_RIGHT:
            x_start = image.width - width
            x_end = image.width
            y_start = 0
            y_end = height
        case Corner.LOWER_LEFT:
            x_start = 0
            x_end = width
            y_start = image.height - height
            y_end = image.height
        case Corner.LOWER_RIGHT:
            x_start = image.width - width
            x_end = image.width
            y_start = image.height - height
            y_end = image.height

    region = image.crop((x_start, y_start, x_end, y_end))
    return region


def avg(numbers: tuple | list) -> float:
    return sum(numbers) / len(numbers)


def add_watermark(image: Image, corner: Corner, watermark: Image,
                  max_width_proportion: float, max_height_proportion: float, opacity: float) -> Image:
    """
    Returns a new image with watermark added in specified corner

    :param image: original image
    :param corner: corner where watermark is added
    :param watermark: watermark to add
    :param max_width_proportion: [0, 1] maximum watermark / image width ratio
    :param max_height_proportion: [0, 1] maximum watermark / image height ratio
    :param opacity: opacity of the watermark
    :return: new image with watermark
    """

    max_width = image.width * max_width_proportion
    max_height = image.height * max_height_proportion

    scale = 1
    if max_height / max_width < watermark.height / watermark.width:
        scale = max_height / watermark.height
    else:
        scale = max_width / watermark.width

    watermark_width = int(watermark.width * scale)
    watermark_height = int(watermark.height * scale)
    watermark = watermark.resize((watermark_width, watermark_height), resample=Image.Resampling.NEAREST)
    # TODO: compare different filters

    alpha = int(255 * opacity)
    watermark.putalpha(alpha)

    # leave the blank pixels at 100% transparency
    transparent_watermark = []
    for item in watermark.getdata():
        if item[:3] == (0, 0, 0):
            transparent_watermark.append((0, 0, 0, 0))
        else:
            transparent_watermark.append(item)
    watermark.putdata(transparent_watermark)

    box = None  # upper left corner
    match corner:
        case Corner.UPPER_LEFT:
            box = (0, 0)
        case Corner.UPPER_RIGHT:
            box = (image.width - watermark.width, 0)
        case Corner.LOWER_LEFT:
            box = (0, image.height - watermark.height)
        case Corner.LOWER_RIGHT:
            box = (image.width - watermark.width, image.height - watermark.height)

    image_with_watermark = Image.new(mode='RGBA', size=image.size, color=(0, 0, 0, 0))
    image_with_watermark.paste(image, (0, 0))
    image_with_watermark.paste(watermark, box, watermark)
    image_with_watermark = image_with_watermark.convert('RGB')

    return image_with_watermark
