import os.path
import sys
import unittest
sys.path.append("../src")

from core.directory_processors import FlatDirectoryProcessor


class TestFlatDirectoryProcessor(unittest.TestCase):

    def setUp(self) -> None:
        self.photos_dir = os.path.abspath('photos')
        self.output_dir = os.path.abspath(os.path.join(self.photos_dir, 'with-watermark'))

        self.processor = FlatDirectoryProcessor(
            max_width_proportion=0.3,
            max_height_proportion=0.3,
            opacity=0.5
        )

    def test_instantiated_correctly(self):
        self.assertIsNotNone(self.processor)

        self.assertTrue(os.path.exists(self.photos_dir), msg='Missing tests photo resources directory')
        self.assertTrue(len(os.listdir(self.photos_dir)) > 0, msg='Missing tests photos')

    def test_creates_output_directory(self):
        self.processor.handle_directory(dir_path=self.photos_dir)
        self.assertTrue(os.path.exists(self.output_dir), msg='Should create output directory')

    def test_processes_all_photos(self):
        self.processor.handle_directory(self.photos_dir)

        original_photos = []
        start_dir = os.getcwd()
        os.chdir(self.output_dir)
        for file in os.listdir(self.photos_dir):
            _, extension = os.path.splitext(file)

            if extension in FlatDirectoryProcessor.SUPPORTED_PHOTO_FILE_FORMATS:
                original_photos.append(file)

        output_photos = os.listdir(self.output_dir)
        self.assertEqual(len(original_photos), len(output_photos), msg='Should have the same number of photos')
        os.chdir(start_dir)


if __name__ == '__main__':
    unittest.main()
