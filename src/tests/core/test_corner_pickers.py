import os.path
from unittest import TestCase

from PIL import Image

from core.corner_pickers import RgbStdevCornerPicker
from core.watermarking import Corner
from tests.resources.sample_photos import SAMPLE_PHOTOS_DIR


class TestRgbStdevCornerPicker(TestCase):

    def setUp(self) -> None:
        self.bottom_uniform = Image.open(os.path.join(SAMPLE_PHOTOS_DIR, 'bottom-uniform-light.jpg'))
        self.left_uniform = Image.open(os.path.join(SAMPLE_PHOTOS_DIR, 'left-uniform-dark.jpg'))
        self.right_uniform = Image.open(os.path.join(SAMPLE_PHOTOS_DIR, 'right-uniform-dark.jpg'))
        self.top_uniform = Image.open(os.path.join(SAMPLE_PHOTOS_DIR, 'top-uniform-light.jpg'))

    def tearDown(self) -> None:
        self.bottom_uniform.close()
        self.left_uniform.close()
        self.right_uniform.close()
        self.top_uniform.close()

    def test_pick_best_corner(self):
        picker = RgbStdevCornerPicker([Corner.UPPER_LEFT, Corner.LOWER_LEFT], 0.15, 0.15)

        self.assertEqual(picker.pick_best_corner(self.bottom_uniform), Corner.LOWER_LEFT,
                         "Should pick the bottom-left uniform corner")
        self.assertIn(picker.pick_best_corner(self.left_uniform), [Corner.UPPER_LEFT, Corner.LOWER_LEFT],
                      "Should pick either of the uniform corners on the left side")
        self.assertIn(picker.pick_best_corner(self.right_uniform), [Corner.UPPER_LEFT, Corner.LOWER_LEFT],
                      "Should pick either of the non-uniform left corners")
        self.assertEqual(picker.pick_best_corner(self.top_uniform), Corner.UPPER_LEFT,
                         "Should pick the upper-left uniform corner")

    def test_raises_exception_with_invalid_ratios(self):
        with self.assertRaisesRegex(ValueError, "must be between 0 and 1"):
            RgbStdevCornerPicker([Corner.UPPER_LEFT], 1.5, 0.1)

        with self.assertRaisesRegex(ValueError, "must be between 0 and 1"):
            RgbStdevCornerPicker([Corner.UPPER_LEFT], 100, 20)

        with self.assertRaisesRegex(ValueError, "must be between 0 and 1"):
            RgbStdevCornerPicker([Corner.UPPER_LEFT], -0.1, 0.1)

    def test_raises_exception_with_no_corners(self):
        with self.assertRaisesRegex(ValueError, "Must provide at least one corner"):
            RgbStdevCornerPicker([], 0.1, 0.1)
