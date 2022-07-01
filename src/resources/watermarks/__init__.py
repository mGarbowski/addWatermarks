import os

WATERMARKS_DIR = os.path.split(__file__)[0]
DEFAULT_LIGHT_WATERMARK = os.path.join(WATERMARKS_DIR, 'watermark-light.png')
DEFAULT_DARK_WATERMARK = os.path.join(WATERMARKS_DIR, 'watermark-dark.png')
