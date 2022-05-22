import os
import sys
import argparse
from enum import Enum
from math import sqrt
from PIL import Image


class Watermark(Enum):
    DARK: Image = Image.open('watermark-dark.png', formats=['PNG'])
    LIGHT: Image = Image.open('watermark-light.png', formats=['PNG'])


class Corner(Enum):
    UPPER_LEFT = 'upper left'
    UPPER_RIGHT = 'upper right'
    LOWER_LEFT = 'lower left'
    LOWER_RIGHT = 'lower right'


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
        -> tuple[Corner, Watermark]:
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
    watermark = Watermark.DARK if params['avg'] > cutoff_color else Watermark.LIGHT
    return corner, watermark


def add_watermark(image: Image, corner: Corner, watermark: Watermark,
                  max_width_proportion=0.15, max_height_proportion=0.15, opacity=0.5) -> Image:
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
    watermark = watermark.value

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

    transparent = Image.new(mode='RGBA', size=image.size, color=(0, 0, 0, 0))
    transparent.paste(image, (0, 0))
    transparent.paste(watermark, box, watermark)
    transparent = transparent.convert('RGB')

    return transparent


def add_best_watermark(image: Image, max_width_proportion=0.15, max_height_proportion=0.15, opacity=0.5) -> Image:
    """
    Add best suited watermark in best suited corner of the image

    :param image: original image
    :param max_width_proportion: [0, 1] maximum watermark / image width ratio
    :param max_height_proportion: [0, 1] maximum watermark / image height ratio
    :param opacity: opacity of the watermark
    :return: new image with watermark
    """

    corner, watermark = best_corner(image, max_width_proportion, max_height_proportion)
    image_with_watermark = add_watermark(image, corner, watermark, max_width_proportion, max_height_proportion, opacity)
    return image_with_watermark


def handle_directory(dir_path: str, max_width_proportion=0.15, max_height_proportion=0.15, opacity=0.5) -> None:
    """
    Add watermarks to all images in directory and save them to a subdirectory
    Photo is saved in the same format

    :param dir_path: directory with photos
    :param max_width_proportion: [0, 1] maximum watermark / image width ratio
    :param max_height_proportion: [0, 1] maximum watermark / image height ratio
    :param opacity: opacity of the watermark
    """

    try:
        os.chdir(dir_path)
    except OSError:
        print(f'Could not open {dir_path}, exiting...')
        sys.exit()

    watermarked_dir = 'with-watermark'
    try:
        os.mkdir(watermarked_dir)
    except FileExistsError:
        pass

    files = os.listdir()

    print(f'Adding watermarks to photos in {dir_path}')

    for file in files:
        filename, extension = os.path.splitext(file)
        if extension in ('.jpg', '.jpeg'):
            image = Image.open(file)
            image_with_watermark = add_best_watermark(image, max_width_proportion, max_height_proportion, opacity)
            image_with_watermark.save(f'{watermarked_dir}/{filename}_watermark{extension}', quality=100)
            print(f'Added watermark to {file}')

    print(f'Saved all watermarked photos to {dir_path}/{watermarked_dir}')


def main():
    parser = argparse.ArgumentParser(description='Adds watermark to each photo in a folder, supports .jpg files')
    parser.add_argument('-f', '--folder', dest='folder', default='.', help='Path to a folder with photos', type=str)
    parser.add_argument('--width', dest='width', default=0.15, help='[0.0, 1.0] Max watermark to image width ratio', type=float)
    parser.add_argument('--height', dest='height', default=0.15, help='[0.0, 1.0] Max watermark to image height ratio', type=float)
    parser.add_argument('-o', '--opacity', dest='opacity', default=0.5, help='[0.0, 1.0] Watermark opacity', type=float)
    args = parser.parse_args()

    if not os.path.exists(args.folder):
        print(f'{args.folder} does not exist')
        sys.exit()

    if not os.path.isdir(args.folder):
        print(f'{args.folder} is not a directory')
        sys.exit()

    handle_directory(args.folder, args.width, args.height, args.opacity)


if __name__ == '__main__':
    main()

# TODO: Handling of folders and nested folders via CLI
# TODO: Optimize by concurrent processing
# TODO: Support other file formats
# TODO: Support providing custom watermarks
# TODO: Support handling single files
