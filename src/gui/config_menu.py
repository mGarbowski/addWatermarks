import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Frame
from typing import Callable

from core.watermarking import Corner
from gui.corner_menu import CornerConfigMenu
from gui.proportion_widget import ProportionWidget
from gui.watermark_widget import WatermarkWidget
from resources.watermarks import DEFAULT_LIGHT_WATERMARK, DEFAULT_DARK_WATERMARK


class ConfigMenu(ttk.Frame):
    """
    UI component for setting configuration parameters:
    watermarks, width, height, opacity and corners where watermarks will be placed
    """

    def __init__(self, container: Frame, display_error: Callable):
        """
        :param container: parent UI component
        :param display_error: callback function, handles displaying error messages
        """

        super().__init__(container)
        self.display_error = display_error

        self.widget_dark = WatermarkWidget(self, "Dark:", DEFAULT_DARK_WATERMARK, self.display_error)
        self.widget_light = WatermarkWidget(self, "Light:", DEFAULT_LIGHT_WATERMARK, self.display_error)
        self.width_widget = ProportionWidget(self, label="Width:", default_value=0.15)
        self.height_widget = ProportionWidget(self, label="Height:", default_value=0.15)
        self.opacity_widget = ProportionWidget(self, label="Opacity:", default_value=0.5)
        self.corner_config_menu = CornerConfigMenu(self)

        self.widget_dark.grid(row=0, column=0, columnspan=3)
        self.widget_light.grid(row=1, column=0, columnspan=3)
        self.width_widget.grid(row=2, column=0, columnspan=3, sticky=tk.W)
        self.height_widget.grid(row=3, column=0, columnspan=3, sticky=tk.W)
        self.opacity_widget.grid(row=4, column=0, columnspan=3, sticky=tk.W)
        self.corner_config_menu.grid(row=5, columnspan=3)

    def get_corners(self) -> list[Corner]:
        """
        Get selected corners.

        :return: list of selected corners
        """

        return self.corner_config_menu.get_corners()

    def get_width(self) -> float:
        """
        Get selected width.

        :return: max watermark width to image ratio
        """

        return self.width_widget.get_value()

    def get_height(self) -> float:
        """
        Get selected height.

        :return: max watermark height to image ratio
        """

        return self.height_widget.get_value()

    def get_opacity(self) -> float:
        """
        Get selected opacity

        :return: watermark opacity [0.0, 1.0]
        """

        return self.opacity_widget.get_value()

    def get_dark_watermark_filepath(self) -> str:
        """
        Get dark watermark's filepath

        :return: filepath to the dark watermark
        """

        return self.widget_dark.get_watermark_filepath()

    def get_light_watermark_filepath(self) -> str:
        """
        Get light watermark's filepath

        :return: filepath to the light watermark
        """

        return self.widget_light.get_watermark_filepath()
