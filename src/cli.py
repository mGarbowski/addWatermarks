import argparse
import os
import sys

from corner_pickers import RgbStdevCornerPicker
from directory_processors import FlatDirectoryProcessor
from watermark_pickers import AvgRgbWatermarkPicker
from watermarking import Corner

DARK_WATERMARK_FILEPATH = './watermark-dark.png'
LIGHT_WATERMARK_FILEPATH = './watermark-light.png'
DEFAULT_CORNERS = [Corner.UPPER_LEFT, Corner.UPPER_RIGHT, Corner.LOWER_LEFT, Corner.LOWER_RIGHT]
DEFAULT_CUTOFF_COLOR = 150  # TODO: fine tune the cutoff color


def main():
    parser = argparse.ArgumentParser(description='Adds watermark to each photo in a folder, supports .jpg files')
    parser.add_argument('-f', '--folder', dest='folder', default='.', help='Path to a folder with photos', type=str)
    parser.add_argument('--width', dest='width', default=0.15, help='[0.0, 1.0] Max watermark to image width ratio',
                        type=float)
    parser.add_argument('--height', dest='height', default=0.15, help='[0.0, 1.0] Max watermark to image height ratio',
                        type=float)
    parser.add_argument('-o', '--opacity', dest='opacity', default=0.5, help='[0.0, 1.0] Watermark opacity', type=float)
    args = parser.parse_args()

    if not os.path.exists(args.folder):
        print(f'{args.folder} does not exist')
        sys.exit()

    if not os.path.isdir(args.folder):
        print(f'{args.folder} is not a directory')
        sys.exit()

    corner_picker = RgbStdevCornerPicker(corners=DEFAULT_CORNERS,
                                         max_width_proportion=args.width,
                                         max_height_proportion=args.height)

    watermark_picker = AvgRgbWatermarkPicker(max_width_proportion=args.width,
                                             max_height_proportion=args.height,
                                             cutoff_color=DEFAULT_CUTOFF_COLOR)

    directory_processor = FlatDirectoryProcessor(corner_picker=corner_picker,
                                                 watermark_picker=watermark_picker,
                                                 dark_watermark_filepath=DARK_WATERMARK_FILEPATH,
                                                 light_watermark_filepath=LIGHT_WATERMARK_FILEPATH,
                                                 max_width_proportion=args.width,
                                                 max_height_proportion=args.height,
                                                 opacity=args.opacity)

    directory_processor.handle_directory(args.folder)


if __name__ == '__main__':
    main()
