import os.path
from abc import ABC, abstractmethod

from PIL import Image

from corner_pickers import CornerPicker, RgbStdevCornerPicker
from watermark_pickers import WatermarkPicker, WatermarkType, AvgRgbWatermarkPicker
from watermarking import add_watermark, Corner


class DirectoryProcessor(ABC):
    SUPPORTED_PHOTO_FILE_FORMATS = ['.jpg', '.jpeg']
    SUPPORTED_WATERMARK_FILE_FORMATS = ['.png']

    def __init__(self,
                 dark_watermark_filepath: str,
                 light_watermark_filepath: str,
                 max_width_proportion: float,
                 max_height_proportion: float,
                 opacity: float,
                 cutoff_color=150,  # TODO: fine tune the cutoff color
                 corners: list[Corner] = None):
        """
        Checks if watermark files exists and have a valid format
        TODO: May raise Exception

        :param dark_watermark_filepath: path to a file containing dark watermark
        :param light_watermark_filepath: path to a file containing light watermark
        :param max_width_proportion: [0, 1] maximum watermark / image width ratio
        :param max_height_proportion: [0, 1] maximum watermark / image height ratio
        :param opacity: opacity of the watermark
        """

        for file_path in (dark_watermark_filepath, light_watermark_filepath):
            if not os.path.exists(file_path):
                raise ValueError(f"{file_path} does not exist")

            filename, extension = os.path.splitext(file_path)
            if extension not in DirectoryProcessor.SUPPORTED_WATERMARK_FILE_FORMATS:
                raise ValueError(f"Supplied file of invalid type - {extension}, "
                                 f"supported types: {DirectoryProcessor.SUPPORTED_WATERMARK_FILE_FORMATS}")

        # Opening files not checked
        self.dark_watermark = Image.open(dark_watermark_filepath)
        self.light_watermark = Image.open(light_watermark_filepath)

        # Parameters passed down
        self.opacity = opacity
        self.max_height_proportion = max_height_proportion
        self.max_width_proportion = max_width_proportion
        self.cutoff_color = cutoff_color

        if corners is None:
            self.corners = [
                Corner.UPPER_LEFT,
                Corner.UPPER_RIGHT,
                Corner.LOWER_LEFT,
                Corner.LOWER_RIGHT,
            ]
        else:
            self.corners = corners

        # Default implementations
        self.watermark_picker = AvgRgbWatermarkPicker(
            max_width_proportion=self.max_width_proportion,
            max_height_proportion=self.max_height_proportion,
            cutoff_color=self.cutoff_color
        )
        self.corner_picker = RgbStdevCornerPicker(
            corners=self.corners,
            max_width_proportion=self.max_width_proportion,
            max_height_proportion=self.max_height_proportion
        )

    @abstractmethod
    def handle_directory(self, dir_path: str) -> None:
        """
        Creates a folder containing photos from dir_path with watermarks added
        Handles saving files in the appropriate location

        :param dir_path: path to the directory containing photos to process
        """


class FlatDirectoryProcessor(DirectoryProcessor):

    def handle_directory(self, dir_path: str) -> None:
        start_dir = os.getcwd()

        try:
            os.chdir(dir_path)
        except OSError:
            print(f'Could not open {dir_path}, exiting...')
            return

        watermarked_dir = 'with-watermark'
        try:
            os.mkdir(watermarked_dir)
        except FileExistsError:
            pass

        print(f'Adding watermarks to photos in {dir_path}')
        files = os.listdir()

        for file in files:
            filename, extension = os.path.splitext(file)
            if extension in DirectoryProcessor.SUPPORTED_PHOTO_FILE_FORMATS:
                image = Image.open(file)
                best_corner = self.corner_picker.pick_best_corner(image)
                best_watermark_type = self.watermark_picker.pick_best_watermark(image, best_corner)
                best_watermark = self.dark_watermark if best_watermark_type == WatermarkType.DARK \
                    else self.light_watermark

                image_with_watermark = add_watermark(image, best_corner, best_watermark,
                                                     self.max_width_proportion, self.max_height_proportion,
                                                     self.opacity)
                image_with_watermark.save(f'{watermarked_dir}/{filename}_watermark{extension}', quality=100)
                print(f'Added watermark to {file}')

        print(f'Saved all watermarked photos to {dir_path}/{watermarked_dir}')
        os.chdir(start_dir)

# TODO: Handling of folders and nested folders
# TODO: Optimize by concurrent processing
# TODO: Support other file formats
# TODO: Support providing custom watermarks
# TODO: Support handling single files
