import argparse
import os
import sys

from core.directory_processors import FlatDirectoryProcessor
from core.watermarking import Corner
from resources.watermarks import WATERMARKS_DIR


def main():
    parser = argparse.ArgumentParser(description='Adds watermark to each photo in a folder, supports .jpg files.\n'
                                     + f'Watermark files are located in {WATERMARKS_DIR}.\n'
                                     + 'GUI for this application is also available, see README.txt for more info.\n')

    parser.add_argument('-f', '--folder',
                        dest='folder',
                        help='Path to a folder with photos',
                        required=True,
                        type=str)
    parser.add_argument('--width',
                        dest='width',
                        default=0.15,
                        help='[0.0, 1.0] Max watermark to image width ratio',
                        type=float)
    parser.add_argument('--height',
                        dest='height',
                        default=0.15,
                        help='[0.0, 1.0] Max watermark to image height ratio',
                        type=float)
    parser.add_argument('-o', '--opacity',
                        dest='opacity',
                        default=0.5,
                        help='[0.0, 1.0] Watermark opacity (0 - transparent, 1 - opaque)',
                        type=float)
    parser.add_argument('-c', '--corners',
                        dest='corners',
                        default='top',
                        type=str,
                        choices=['all', 'top', 'bottom', 'left', 'right',
                                 'upper-left', 'upper-right', 'bottom-left', 'bottom-right'])

    args = parser.parse_args()

    if not os.path.exists(args.folder):
        print(f'{args.folder} does not exist')
        sys.exit()

    if not os.path.isdir(args.folder):
        print(f'{args.folder} is not a directory')
        sys.exit()

    corners = None
    match args.corners:
        case 'all':
            corners = [Corner.UPPER_LEFT, Corner.UPPER_RIGHT, Corner.LOWER_LEFT, Corner.LOWER_RIGHT]
        case 'top':
            corners = [Corner.UPPER_LEFT, Corner.UPPER_RIGHT]
        case 'bottom':
            corners = [Corner.LOWER_LEFT, Corner.LOWER_RIGHT]
        case 'left':
            corners = [Corner.UPPER_LEFT, Corner.LOWER_LEFT]
        case 'right':
            corners = [Corner.UPPER_RIGHT, Corner.LOWER_RIGHT]
        case 'upper-left':
            corners = [Corner.UPPER_LEFT]
        case 'upper-right':
            corners = [Corner.UPPER_RIGHT]
        case 'bottom-left':
            corners = [Corner.LOWER_LEFT]
        case 'bottom-right':
            corners = [Corner.LOWER_RIGHT]

    directory_processor = FlatDirectoryProcessor(
        max_width_proportion=args.width,
        max_height_proportion=args.height,
        opacity=args.opacity,
        corners=corners,
    )

    directory_processor.handle_directory(args.folder)


if __name__ == '__main__':
    main()
