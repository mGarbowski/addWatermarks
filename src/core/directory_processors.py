import os.path
from abc import ABC, abstractmethod

from PIL import Image

from core.exceptions import NotSupportedFileFormatException
from resources.watermarks import DEFAULT_LIGHT_WATERMARK, DEFAULT_DARK_WATERMARK
from core.corner_pickers import RgbStdevCornerPicker
from core.watermark_pickers import WatermarkType, AvgRgbWatermarkPicker
from core.watermarking import add_watermark, Corner


class DirectoryProcessor(ABC):
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
        """

        DirectoryProcessor.__validate_watermark_filepath(dark_watermark_filepath)
        DirectoryProcessor.__validate_watermark_filepath(light_watermark_filepath)

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

    @staticmethod
    def __validate_watermark_filepath(filepath: str):
        """
        Raises value error if the file path does not contain a valid watermark

        :param filepath: path to the watermark file
        """
        if not os.path.exists(filepath):
            raise ValueError(f"{filepath} does not exist")

        filename, extension = os.path.splitext(filepath)
        if extension not in DirectoryProcessor.SUPPORTED_WATERMARK_FILE_FORMATS:
            raise ValueError(f"Supplied file of invalid type - {extension}, "
                             f"supported types: {DirectoryProcessor.SUPPORTED_WATERMARK_FILE_FORMATS}")

    def process_directory(self, dir_path: str) -> None:
        """
        Creates a subdirectory in dir_path, adds watermarks to photos and saves them there

        :param dir_path: path to the directory containing photos to process
        """

        dir_path = os.path.abspath(dir_path)
        watermarked_dir = os.path.join(dir_path, 'with-watermark')
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
                self.process_file(filepath, watermarked_dir)
            except NotSupportedFileFormatException as exc:
                print(f"{exc}, skipping {filepath}")
            except OSError as err:
                print(err)

        print(f"Saved all watermarked photos to {watermarked_dir}")

    def process_file(self, filepath: str, output_directory: str) -> None:
        """
        Add watermark to a photo and save it in the specified directory.
        Does not modify the original file.

        :param filepath: path to the photo to process
        :param output_directory: directory where the processed photo will be saved
        :raises NotSupportedFileFormatException: if the file format is not supported
        :raises OSError: if the file could not be written
        """

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
        watermarked_filepath = os.path.join(output_directory, f"{filename}_watermark{extension}")
        watermarked_image.save(watermarked_filepath, quality=100)
        print(f"Added watermark to {base_filename}")

        watermarked_image.close()
        image.close()


class FlatDirectoryProcessor(DirectoryProcessor):
    pass
    # def process_directory(self, dir_path: str) -> None:
    #     start_dir = os.getcwd()
    #
    #     os.chdir(dir_path)
    #
    #     watermarked_dir = '../../tests/photos/with-watermark'
    #     try:
    #         os.mkdir(watermarked_dir)
    #     except FileExistsError:
    #         pass
    #
    #     print(f'Adding watermarks to photos in {dir_path}')
    #     files = os.listdir()
    #
    #     for file in files:
    #         filename, extension = os.path.splitext(file)
    #         if extension in DirectoryProcessor.SUPPORTED_PHOTO_FILE_FORMATS:
    #             image = Image.open(file)
    #             best_corner = self.corner_picker.pick_best_corner(image)
    #             best_watermark_type = self.watermark_picker.pick_best_watermark(image, best_corner)
    #             best_watermark = self.dark_watermark if best_watermark_type == WatermarkType.DARK \
    #                 else self.light_watermark
    #
    #             image_with_watermark = add_watermark(image, best_corner, best_watermark,
    #                                                  self.max_width_proportion, self.max_height_proportion,
    #                                                  self.opacity)
    #             image_with_watermark.save(f'{watermarked_dir}/{filename}_watermark{extension}', quality=100)
    #             print(f'Added watermark to {file}')
    #
    #     print(f'Saved all watermarked photos to {dir_path}/{watermarked_dir}')  # TODO: fix log message
    #     os.chdir(start_dir)

# TODO: Handling of folders and nested folders
# TODO: Optimize by concurrent processing
# TODO: Support other file formats
# TODO: Support providing custom watermarks
# TODO: Support handling single files
