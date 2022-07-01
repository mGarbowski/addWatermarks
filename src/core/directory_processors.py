import os.path
from typing import Optional

import PIL.Image
from PIL import Image

from core.corner_pickers import RgbStdevCornerPicker
from core.exceptions import NotSupportedFileFormatException
from core.watermark_pickers import WatermarkType, AvgRgbWatermarkPicker
from core.watermarking import add_watermark, Corner
from resources.watermarks import DEFAULT_LIGHT_WATERMARK, DEFAULT_DARK_WATERMARK


class DirectoryProcessor:
    SUPPORTED_PHOTO_FILE_FORMATS = ['.jpg', '.jpeg']
    SUPPORTED_WATERMARK_FILE_FORMATS = ['.png']

    def __init__(self,
                 max_width_proportion: float,
                 max_height_proportion: float,
                 opacity: float,
                 dark_watermark_filepath: str = DEFAULT_DARK_WATERMARK,
                 light_watermark_filepath: str = DEFAULT_LIGHT_WATERMARK,
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
        :raises FileNotFoundError: if provided watermark could not be found
        :raises NotSupportedFileFormatException: if provided watermark's type is not supported
        """

        DirectoryProcessor.__validate_watermark_filepath(dark_watermark_filepath)
        DirectoryProcessor.__validate_watermark_filepath(light_watermark_filepath)

        # Files will only be loaded when needed
        self.dark_watermark_filepath = dark_watermark_filepath
        self.light_watermark_filepath = light_watermark_filepath
        self.dark_watermark: Optional[PIL.Image.Image] = None
        self.light_watermark: Optional[PIL.Image.Image] = None

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

    @staticmethod
    def __validate_watermark_filepath(filepath: str):
        """
        Raises value error if the file path does not contain a valid watermark

        :param filepath: path to the watermark file
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"{filepath} does not exist")

        filename, extension = os.path.splitext(filepath)
        if extension not in DirectoryProcessor.SUPPORTED_WATERMARK_FILE_FORMATS:
            raise NotSupportedFileFormatException(f"Supported file formats for watermarks are: "
                                                  + f"{', '.join(DirectoryProcessor.SUPPORTED_WATERMARK_FILE_FORMATS)}")

    def process_directory(self, dir_path: str, output_dir: Optional[str] = None) -> None:
        """
        Adds watermarks to photos in dir_path and saves them in the output_dir.
        By default, files will be saved in a subdirectory of dir_path

        :param dir_path: path to the directory containing photos to process
        :param output_dir:
        """

        # Loading watermarks
        if self.dark_watermark is None:
            self.dark_watermark = Image.open(self.dark_watermark_filepath)
        if self.light_watermark is None:
            self.light_watermark = Image.open(self.light_watermark_filepath)

        dir_path = os.path.abspath(dir_path)
        watermarked_dir = os.path.join(dir_path, 'with-watermark') if output_dir is None else output_dir
        try:
            os.mkdir(watermarked_dir)
            print(f"Creating {watermarked_dir}")
        except FileExistsError:
            print(f"{watermarked_dir} already exists")

        print(f"Watermarked photos will be saved to {watermarked_dir}")

        directory_contents = [os.path.join(dir_path, file) for file in os.listdir(dir_path)]
        files = [file for file in directory_contents if os.path.isfile(file)]
        for filepath in files:
            try:
                self._process_file(filepath, watermarked_dir)
            except NotSupportedFileFormatException as exc:
                print(f"{exc}, skipping {filepath}")
            except OSError as err:
                print(err)

        print(f"Saved all watermarked photos to {watermarked_dir}")

        # Closing watermarks
        self.dark_watermark.close()
        self.dark_watermark = None
        self.light_watermark.close()
        self.light_watermark = None

    def _process_file(self, filepath: str, output_directory: str, suffix: str = "_watermark") -> None:
        """
        Add watermark to a photo and save it in the specified directory.
        Does not modify the original file.

        Requires self.dark_watermark and self.light_watermark to be open.
        Use :method:`DirectoryProcessor.process_single_file` as part of the public API

        :param filepath: path to the photo to process
        :param output_directory: directory where the processed photo will be saved
        :param suffix: suffix added to the processed photo's filename
        :raises NotSupportedFileFormatException: if the file format is not supported
        :raises OSError: if the file could not be written
        """

        assert self.dark_watermark is not None
        assert self.light_watermark is not None

        base_filename = os.path.basename(filepath)
        filename, extension = os.path.splitext(base_filename)

        if extension not in DirectoryProcessor.SUPPORTED_PHOTO_FILE_FORMATS:
            raise NotSupportedFileFormatException(
                f"Supported file formats are: {', '.join(DirectoryProcessor.SUPPORTED_PHOTO_FILE_FORMATS)}"
            )

        image = Image.open(filepath)
        corner = self.corner_picker.pick_best_corner(image)
        watermark_type = self.watermark_picker.pick_best_watermark(image, corner)
        watermark = self.dark_watermark if watermark_type == WatermarkType.DARK else self.light_watermark

        watermarked_image = add_watermark(image=image,
                                          corner=corner,
                                          watermark=watermark,
                                          max_width_proportion=self.max_width_proportion,
                                          max_height_proportion=self.max_height_proportion,
                                          opacity=self.opacity)
        watermarked_filepath = os.path.join(output_directory, f"{filename}{suffix}{extension}")
        watermarked_image.save(watermarked_filepath, quality=100)
        print(f"Added watermark to {base_filename}")

        watermarked_image.close()
        image.close()

    def process_single_file(self, filepath: str, output_directory: str, suffix: str = "_watermark") -> None:
        """
        Processes a single file, adds watermark and saves in output_directory.
        Does not modify the original file.

        :param filepath: path to the photo to process
        :param output_directory: directory where the processed photo will be saved
        :param suffix: suffix added to the processed photo's filename
        :raises NotSupportedFileFormatException: if the file format is not supported
        :raises OSError: if the file could not be written
        """

        self._open_watermarks()
        self._process_file(filepath, output_directory, suffix)
        self._close_watermarks()

    def _open_watermarks(self) -> None:
        """
        Safely open watermark files. For internal use with :method:`core.DirectoryProcessor.process_single_file`
        """

        if self.dark_watermark is None:
            self.dark_watermark = Image.open(self.dark_watermark_filepath)
        if self.light_watermark is None:
            self.light_watermark = Image.open(self.light_watermark_filepath)

    def _close_watermarks(self) -> None:
        """
        Safely close watermark files. For internal use with :method:`core.DirectoryProcessor.process_single_file`
        """

        if self.dark_watermark is not None:
            self.dark_watermark.close()
            self.dark_watermark = None
        if self.light_watermark is not None:
            self.light_watermark.close()
            self.light_watermark = None

# TODO: Handling of folders and nested folders
# TODO: Optimize by concurrent processing
