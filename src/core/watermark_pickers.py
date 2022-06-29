from abc import ABC, abstractmethod
from enum import Enum

from PIL import Image

from core.watermarking import Corner, cut_corner, avg, average_colors


class WatermarkType(Enum):
    DARK = 0
    LIGHT = 1


class WatermarkPicker(ABC):
    """
    Picks the best watermark to add to a given image
    "best" is determined according to implementation's spec
    Options are either light or dark

    """

    def __init__(self, max_width_proportion: float, max_height_proportion: float):
        if not 0 <= max_width_proportion <= 1:
            raise ValueError('width_proportion must be between [0.0, 1.0]')
        if not 0 <= max_height_proportion <= 1:
            raise ValueError('height_proportion must be between [0.0, 1.0]')

        self.max_height_proportion = max_height_proportion
        self.max_width_proportion = max_width_proportion

    @abstractmethod
    def pick_best_watermark(self, image: Image, corner: Corner) -> WatermarkType:
        """
        Picks the best watermark type to add to an image in a given corner

        :param image: image to be watermarked
        :param corner: corner where watermark will be placed
        :return: best watermark type to add in a given corner to the given image
        """


class AvgRgbWatermarkPicker(WatermarkPicker):
    """
    Picks the best watermark type based on the average RGB colors value in a given corner
    """

    def __init__(self, max_width_proportion: float, max_height_proportion: float, cutoff_color: int):
        if not 0 <= cutoff_color <= 255:
            raise ValueError("cutoff_color must be a valid RGB color value - integer [0, 255]")

        super().__init__(max_width_proportion, max_height_proportion)
        self.cutoff_color = cutoff_color

    def pick_best_watermark(self, image: Image, corner: Corner) -> WatermarkType:
        corner_img = cut_corner(image, corner, self.max_width_proportion, self.max_height_proportion)
        avg_color = avg(average_colors(corner_img))

        best_watermark_type = WatermarkType.DARK if avg_color > self.cutoff_color else WatermarkType.LIGHT
        return best_watermark_type
