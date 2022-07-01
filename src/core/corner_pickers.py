from abc import ABC, abstractmethod

from PIL import Image

from core.watermarking import cut_corner, colors_stdev, avg, Corner


class CornerPicker(ABC):
    """
    An object that picks the best corner of an image to place a watermark
    "best" is determined by implementation's spec
    """

    def __init__(self,
                 corners: list[Corner],
                 max_width_proportion: float,
                 max_height_proportion: float):
        """
        Validates inputs

        :param corners: list of corners for the picker to choose from
        :param max_width_proportion: [0.0, 1.0] maximum watermark / image width ratio
        :param max_height_proportion: [0.0, 1.0] maximum watermark / image height ratio
        """
        if not 0 <= max_width_proportion <= 1:
            raise ValueError("width_proportion must be between 0 and 1")
        if not 0 <= max_height_proportion <= 1:
            raise ValueError("height_proportion must be between 0 and 1")
        if len(corners) < 1:
            raise ValueError("Must provide at least one corner")

        self.height_proportion = max_height_proportion
        self.width_proportion = max_width_proportion
        self.corners = corners

    @abstractmethod
    def pick_best_corner(self, image: Image) -> Corner:
        """
        Picks the best corner of an image to place a watermark

        :param image: image to choose a corner from
        :return: best corner chosen according to implementation's spec,
                (UPPER_LEFT, UPPER_RIGHT, LOWER_LEFT, LOWER_RIGHT)
        """


class RgbStdevCornerPicker(CornerPicker):
    """
    Picks corner with the smallest average standard deviation of RGB color values
    """

    def pick_best_corner(self, image: Image) -> Corner:
        standard_deviations = {}
        for corner in self.corners:
            corner_img = cut_corner(image, corner, self.width_proportion, self.height_proportion)
            avg_std = avg(colors_stdev(corner_img))
            standard_deviations[corner] = avg_std

        best_corner, min_std = min(standard_deviations.items(), key=lambda it: it[1])
        return best_corner
