import os.path
import shutil
import tempfile
from unittest import TestCase

from PIL import Image

from core.directory_processors import DirectoryProcessor
from core.exceptions import NotSupportedFileFormatException
from tests.resources.sample_photos import SAMPLE_PHOTOS_DIR


class TestDirectoryProcessor(TestCase):

    def setUp(self) -> None:
        # Use default values if possible
        self.processor = DirectoryProcessor(max_width_proportion=0.15,
                                            max_height_proportion=0.15,
                                            opacity=0.5)

        self.photos_dir = tempfile.mkdtemp()
        self.output_dir = tempfile.mkdtemp()

        shutil.copy(os.path.join(SAMPLE_PHOTOS_DIR, "white.jpg"), self.photos_dir)
        shutil.copy(os.path.join(SAMPLE_PHOTOS_DIR, "black.jpg"), self.photos_dir)
        shutil.copy(os.path.join(SAMPLE_PHOTOS_DIR, "illegal-format.png"), self.photos_dir)
        shutil.copy(os.path.join(SAMPLE_PHOTOS_DIR, "bottom-uniform-light.jpg"), self.photos_dir)
        shutil.copy(os.path.join(SAMPLE_PHOTOS_DIR, "left-dark-right-light.jpg"), self.photos_dir)
        shutil.copy(os.path.join(SAMPLE_PHOTOS_DIR, "left-uniform-dark.jpg"), self.photos_dir)
        shutil.copy(os.path.join(SAMPLE_PHOTOS_DIR, "right-uniform-dark.jpg"), self.photos_dir)
        shutil.copy(os.path.join(SAMPLE_PHOTOS_DIR, "top-uniform-light.jpg"), self.photos_dir)

    def test_process_single_file_jpg(self):
        filepath_black = os.path.join(self.photos_dir, "black.jpg")
        filepath_white = os.path.join(self.photos_dir, "white.jpg")

        self.processor.process_single_file(filepath_black, self.output_dir)
        self.assertIn("black_watermark.jpg", os.listdir(self.output_dir),
                      "Should save watermarked file with the default suffix")

        self.processor.process_single_file(filepath_white, self.output_dir, suffix="_mysuffix")
        self.assertIn("white_mysuffix.jpg", os.listdir(self.output_dir),
                      "Should save watermarked file with custom suffix")

        original_white = Image.open(filepath_white)
        watermarked_white = Image.open(os.path.join(self.output_dir, "white_mysuffix.jpg"))
        self.assertNotEqual(list(original_white.getdata()), list(watermarked_white.getdata()),
                            "Files should have different contents")

        original_black = Image.open(filepath_black)
        watermarked_black = Image.open(os.path.join(self.output_dir, "black_watermark.jpg"))
        self.assertNotEqual(list(original_black.getdata()), list(watermarked_black.getdata()),
                            "Files should have different contents")

        # Cleanup
        original_black.close()
        watermarked_black.close()
        original_white.close()
        watermarked_white.close()

    def test_process_single_file_png(self):
        filepath_illegal = os.path.join(self.photos_dir, "illegal-format.png")

        with self.assertRaisesRegex(NotSupportedFileFormatException, "Supported file formats are"):
            self.processor.process_single_file(filepath_illegal, self.output_dir,
                                               "Should raise exception on illegal file format")

    def test_process_directory(self):
        self.assertEqual(len(os.listdir(self.photos_dir)), 8, "Set up correctly")

        self.processor.process_directory(self.photos_dir)
        self.assertIn("with-watermark", os.listdir(self.photos_dir),
                      "Should create the default subdirectory")

        watermarked_directory = os.path.join(self.photos_dir, "with-watermark")
        self.assertEqual(len(os.listdir(watermarked_directory)), 7,
                         "Should process all jpg files and skip the png")
