import os
import sys
from unittest import TestCase

from PIL import Image

from core.watermark_pickers import AvgRgbWatermarkPicker, WatermarkType
from core.watermarking import Corner
from tests.resources.sample_photos import SAMPLE_PHOTOS_DIR


# noinspection DuplicatedCode
class TestAvgRgbWatermarkPicker(TestCase):

    def setUp(self) -> None:
        self.bottom_light = Image.open(os.path.join(SAMPLE_PHOTOS_DIR, 'bottom-uniform-light.jpg'))
        self.left_dark = Image.open(os.path.join(SAMPLE_PHOTOS_DIR, 'left-uniform-dark.jpg'))
        self.left_dark_right_light = Image.open(os.path.join(SAMPLE_PHOTOS_DIR, 'left-dark-right-light.jpg'))

    def tearDown(self) -> None:
        self.bottom_light.close()
        self.left_dark.close()
        self.left_dark_right_light.close()

    def test_raises_exception_with_invalid_color(self):
        with self.assertRaisesRegex(ValueError, "cutoff_color must be a valid RGB color value"):
            AvgRgbWatermarkPicker(0.1, 0.1, cutoff_color=300)

        with self.assertRaisesRegex(ValueError, "cutoff_color must be a valid RGB color value"):
            AvgRgbWatermarkPicker(0.1, 0.1, cutoff_color=-10)

    def test_raises_exception_with_invalid_ratios(self):
        with self.assertRaisesRegex(ValueError, "must be between 0 and 1"):
            AvgRgbWatermarkPicker(1.5, 0.1)

        with self.assertRaisesRegex(ValueError, "must be between 0 and 1"):
            AvgRgbWatermarkPicker(0.1, 3)

        with self.assertRaisesRegex(ValueError, "must be between 0 and 1"):
            AvgRgbWatermarkPicker(-1, 0.99)

        with self.assertRaisesRegex(ValueError, "must be between 0 and 1"):
            AvgRgbWatermarkPicker(-1.5, -0.1)

    def test_pick_best_watermark(self):
        picker = AvgRgbWatermarkPicker(0.1, 0.1)

        self.assertEqual(picker.pick_best_watermark(self.bottom_light, Corner.LOWER_LEFT), WatermarkType.DARK,
                         "Should choose dark watermark on light background")
        self.assertEqual(picker.pick_best_watermark(self.bottom_light, Corner.LOWER_RIGHT), WatermarkType.DARK,
                         "Should choose dark watermark on light background")

        self.assertEqual(picker.pick_best_watermark(self.left_dark, Corner.LOWER_LEFT), WatermarkType.LIGHT,
                         "Should choose light watermark on dark background")
        self.assertEqual(picker.pick_best_watermark(self.left_dark, Corner.UPPER_LEFT), WatermarkType.LIGHT,
                         "Should choose light watermark on dark background")

        self.assertEqual(picker.pick_best_watermark(self.left_dark_right_light, Corner.UPPER_LEFT), WatermarkType.LIGHT,
                         "Should choose light watermark on dark background")
        self.assertEqual(picker.pick_best_watermark(self.left_dark_right_light, Corner.UPPER_RIGHT), WatermarkType.DARK,
                         "Should choose dark watermark on light background")
        self.assertEqual(picker.pick_best_watermark(self.left_dark_right_light, Corner.LOWER_RIGHT), WatermarkType.DARK,
                         "Should choose dark watermark on light background")
        self.assertEqual(picker.pick_best_watermark(self.left_dark_right_light, Corner.LOWER_LEFT), WatermarkType.LIGHT,
                         "Should choose light watermark on dark background")
