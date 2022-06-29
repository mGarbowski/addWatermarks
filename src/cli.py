import argparse
import os
import sys

from core.directory_processors import FlatDirectoryProcessor
from core.watermarking import Corner


def main():
    parser = argparse.ArgumentParser(description='Adds watermark to each photo in a folder, supports .jpg files')
    parser.add_argument('-f', '--folder',
                        dest='folder',
                        default='.',
                        help='Path to a folder with photos',
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
                        help='[0.0, 1.0] Watermark opacity',
                        type=float)
    parser.add_argument('-c', '--corner', '--corners',
                        dest='corners',
                        default='top',
                        type=str,
                        choices=['all', 'top', 'bottom', 'left', 'right',
                                 'upper-left', 'upper-right', 'bottom-left', 'bottom-right'],)

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
