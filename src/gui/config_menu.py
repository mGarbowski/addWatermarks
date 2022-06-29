import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Label

from gui.corner_menu import CornerConfigMenu
from gui.proportion_widget import ProportionWidget
from gui.watermark_widget import WatermarkWidget
from resources.watermarks import DEFAULT_LIGHT_WATERMARK, DEFAULT_DARK_WATERMARK


class ConfigMenu(ttk.Frame):

    def __init__(self, container, error_callback):
        super().__init__(container)
        self.error_callback = error_callback

        self.widget_dark = WatermarkWidget(self, "Dark:", DEFAULT_DARK_WATERMARK, self.error_callback)
        self.widget_light = WatermarkWidget(self, "Light:", DEFAULT_LIGHT_WATERMARK, self.error_callback)
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

    def get_corners(self):
        return self.corner_config_menu.get_corners()

    def get_width(self):
        return self.width_widget.get_value()

    def get_height(self):
        return self.height_widget.get_value()

    def get_opacity(self):
        return self.opacity_widget.get_value()

    def get_dark_watermark_filepath(self):
        return self.widget_dark.get_watermark_filepath()

    def get_light_watermark_filepath(self):
        return self.widget_light.get_watermark_filepath()
