import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Label

from gui.corner_menu import CornerConfigMenu
from gui.proportion_entry import ProportionEntry
from gui.watermark_widget import WatermarkWidget
from resources.watermarks import DEFAULT_LIGHT_WATERMARK, DEFAULT_DARK_WATERMARK


class ConfigMenu(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)
        self.error_callback = container.set_error_message

        self.widget_dark = WatermarkWidget(self, "Dark:", DEFAULT_DARK_WATERMARK, self.error_callback)
        self.widget_light = WatermarkWidget(self, "Light:", DEFAULT_LIGHT_WATERMARK, self.error_callback)
        self.widget_dark.grid(row=0, column=0, columnspan=3)
        self.widget_light.grid(row=1, column=0, columnspan=3)

        self.width_label = Label(self, text="Width:")
        self.height_label = Label(self, text="Height:")
        self.opacity_label = Label(self, text="Opacity:")
        self.width_entry = ProportionEntry(self, default_value=0.15)
        self.height_entry = ProportionEntry(self, default_value=0.15)
        self.opacity_entry = ProportionEntry(self, default_value=0.5)

        self.width_label.grid(row=2, column=0, sticky=tk.W)
        self.height_label.grid(row=3, column=0, sticky=tk.W)
        self.opacity_label.grid(row=4, column=0, sticky=tk.W)
        self.width_entry.grid(row=2, column=1, columnspan=2, sticky=tk.E)
        self.height_entry.grid(row=3, column=1, columnspan=2, sticky=tk.E)
        self.opacity_entry.grid(row=4, column=1, columnspan=2, sticky=tk.E)

        self.corner_config_menu = CornerConfigMenu(self)
        self.corner_config_menu.grid(row=5, columnspan=3)

    def get_corners(self):
        return self.corner_config_menu.get_corners()

    def get_width(self):
        return self.width_entry.get_value()

    def get_height(self):
        return self.height_entry.get_value()

    def get_opacity(self):
        return self.opacity_entry.get_value()

    def get_dark_watermark_filepath(self):
        return self.widget_dark.get_watermark_filepath()

    def get_light_watermark_filepath(self):
        return self.widget_light.get_watermark_filepath()
