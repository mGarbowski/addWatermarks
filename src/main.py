from enum import Enum
from math import sqrt
from PIL import Image


class WatermarkType(Enum):
    DARK = 'dark'
    LIGHT = 'light'


class Corner(Enum):
    UPPER_LEFT = 'upper left'
    UPPER_RIGHT = 'upper right'
    LOWER_LEFT = 'lower left'
    LOWER_RIGHT = 'lower right'


def add_watermark(image: Image, watermark: Image) -> Image:
    pass


# def negative():
#     image = Image.open('../sandbox/sample-image.jpeg')
#     source = image.split()
#     R, G, B = 0, 1, 2
#
#     red_inv = source[R].point(lambda i: 255-i)
#     green_inv = source[G].point(lambda i: 255-i)
#     blue_inv = source[B].point(lambda i: 255-i)
#
#     source[R].paste(red_inv, None)
#     source[G].paste(green_inv, None)
#     source[B].paste(blue_inv, None)
#
#     image = Image.merge(image.mode, source)
#     image.save('../sandbox/negative.jpg')


def cut_corner(image: Image, corner: Corner, width_proportion: float, height_proportion: float) -> Image:
    """
    Returns a of the image of specified proportions

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


def _average_colors(image: Image) -> tuple[int, int, int]:
    """
    Average color of an image
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


def average_color(image: Image) -> int:
    rgb_colors = _average_colors(image)
    r, g, b = rgb_colors
    return (r + g + b) // 3


def colors_stdev(image: Image) -> float:
    """
    Average standard deviation of RGB colors in an image
    :param image:
    :return:
    """

    avg_red, avg_green, avg_blue = _average_colors(image)
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

    return (std_red + std_green + std_blue) / 3


def best_corner(image: Image, width_proportion=0.15, height_proportion=0.15, cutoff_color=128)\
        -> tuple[Corner, WatermarkType]:
    """
    Picks the best corner to place watermark in, and either light or dark watermark
    Choice of corner is based on the lowest average standard deviation of colors in the corner
    Choice of watermark type is based on the average color in the corner

    :param image: Image
    :param width_proportion: max width that the watermark can take
    :param height_proportion: max height that the watermark can take
    :param cutoff_color: (optional) average color above which dark watermark is preferred over light
    :return: tuple (best corner, best watermark type)
    """
    # TODO: fine tune the cutoff color
    corners = [Corner.UPPER_LEFT, Corner.UPPER_RIGHT, Corner.LOWER_LEFT, Corner.LOWER_RIGHT]
    corner_params = {}

    for corner in corners:
        corner_img = cut_corner(image, corner, width_proportion, height_proportion)
        avg = average_color(corner_img)
        std = colors_stdev(corner_img)
        corner_params[corner] = {'std': std, 'avg': avg}

    corner, params = min(corner_params.items(), key=lambda c: c[1]['std'])
    watermark_type = WatermarkType.DARK if params['avg'] > cutoff_color else WatermarkType.LIGHT
    return corner, watermark_type


def main():
    image = Image.open('../sandbox/sample-image.jpeg')
    watermark = Image.open('../sandbox/sample-watermark.png')
    image_with_watermark = add_watermark(image, watermark)
    image_with_watermark.save('../sandbox/sample-image-with-watermark.jpg')
    c, w = best_corner(image, 0.15, 0.15)


if __name__ == '__main__':
    main()

# TODO: Implement adding the watermark
# TODO: Implement CLI
# TODO: Handling of folders and nested folders via CLI
# TODO: Optimize by concurrent processing
