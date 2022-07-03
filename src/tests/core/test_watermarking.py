import os
from unittest import TestCase

from PIL import Image

from core.watermarking import cut_corner, Corner, add_watermark
from resources.watermarks import DEFAULT_DARK_WATERMARK
from tests.resources.sample_photos import SAMPLE_PHOTOS_DIR


# noinspection DuplicatedCode
class TestWatermarking(TestCase):
    def setUp(self) -> None:
        self.black = Image.open(os.path.join(SAMPLE_PHOTOS_DIR, 'black.jpg'))
        self.white = Image.open(os.path.join(SAMPLE_PHOTOS_DIR, 'white.jpg'))
        self.dark_watermark = Image.open(DEFAULT_DARK_WATERMARK)

    def tearDown(self) -> None:
        self.black.close()
        self.white.close()
        self.dark_watermark.close()

    def test_cut_corner(self):
        self.assertEqual(self.black.width, 600, "Depends on known size of the image")
        self.assertEqual(self.black.height, 480, "Depends on known size of the image")
        self.assertEqual(self.white.width, 600, "Depends on known size of the image")
        self.assertEqual(self.white.height, 480, "Depends on known size of the image")

        corner = cut_corner(image=self.black,
                            corner=Corner.LOWER_LEFT,
                            width_proportion=0.5,
                            height_proportion=0.1)

        self.assertEqual(corner.width, 300, "Should be 300 pixels wide")
        self.assertEqual(corner.height, 48, "Should be 48 pixels high")
        self.assertEqual(corner.getpixel(xy=(0, 0)), (0, 0, 0), "Should be black")

        corner = cut_corner(image=self.white,
                            corner=Corner.UPPER_RIGHT,
                            width_proportion=0.25,
                            height_proportion=1)

        self.assertEqual(corner.width, 150, "Should be 150 pixels wide")
        self.assertEqual(corner.height, 480, "Should be 480 pixels high")
        self.assertEqual(corner.getpixel(xy=(0, 0)), (255, 255, 255), "Should be white")

    def test_add_watermark(self):
        original_copy = self.white.copy()
        watermarked = add_watermark(image=self.white,
                                    corner=Corner.UPPER_LEFT,
                                    watermark=self.dark_watermark,
                                    max_width_proportion=0.15,
                                    max_height_proportion=0.15,
                                    opacity=0.5)

        self.assertEqual(list(watermarked.getdata()), list(watermarked.getdata()),
                         "Assertion on image data works correctly")
        self.assertEqual(list(self.white.getdata()), list(original_copy.getdata()),
                         "Should not modify the original file")

        non_watermarked_corner = cut_corner(image=watermarked,
                                            corner=Corner.UPPER_RIGHT,
                                            width_proportion=0.15,
                                            height_proportion=0.15)
        original_corner = cut_corner(image=self.white,
                                     corner=Corner.UPPER_RIGHT,
                                     width_proportion=0.15,
                                     height_proportion=0.15)
        self.assertEqual(list(non_watermarked_corner.getdata()), list(original_corner.getdata()),
                         "Top-right corner should be unchanged")

        watermarked_corner = cut_corner(image=watermarked,
                                        corner=Corner.UPPER_LEFT,
                                        width_proportion=0.15,
                                        height_proportion=0.15)
        original_corner = cut_corner(image=self.white,
                                     corner=Corner.UPPER_LEFT,
                                     width_proportion=0.15,
                                     height_proportion=0.15)
        self.assertNotEqual(list(watermarked_corner.getdata()), list(original_corner.getdata()),
                            "Top-left corner should be different than the original")
