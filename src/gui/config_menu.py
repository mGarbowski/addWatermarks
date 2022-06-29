import os.path
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.ttk import Label, Button

from core.directory_processors import DirectoryProcessor
from core.exceptions import NotSupportedFileFormatException
from gui.corner_menu import CornerConfigMenu
from gui.proportion_entry import ProportionEntry
from resources.watermarks import DEFAULT_LIGHT_WATERMARK, DEFAULT_DARK_WATERMARK


class ConfigMenu(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)
        self.error_callback = container.set_error_message

        self.watermark_light_filepath = DEFAULT_LIGHT_WATERMARK
        self.watermark_dark_filepath = DEFAULT_DARK_WATERMARK

        self.dark_label = Label(self, text="Dark:")
        self.dark_status = Label(self, text="Default", width=12)
        self.dark_button = Button(self, text="Change", command=self.browse_dark_watermark)
        self.dark_label.grid(row=0, column=0, sticky=tk.W)
        self.dark_status.grid(row=0, column=1, sticky=tk.W)
        self.dark_button.grid(row=0, column=2)

        self.light_label = Label(self, text="Light:")
        self.light_status = Label(self, text="Default", width=12)
        self.light_button = Button(self, text="Change", command=self.browse_light_watermark)
        self.light_label.grid(row=1, column=0, sticky=tk.W)
        self.light_status.grid(row=1, column=1)
        self.light_button.grid(row=1, column=2)

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

    @staticmethod
    def browse_watermark() -> str:
        filepath = filedialog.askopenfilename()
        filename, extension = os.path.splitext(filepath)
        if extension not in DirectoryProcessor.SUPPORTED_WATERMARK_FILE_FORMATS:
            raise NotSupportedFileFormatException(f"Supported file formats for watermarks are: "
                                                  f"{''.join(DirectoryProcessor.SUPPORTED_WATERMARK_FILE_FORMATS)}")

        return filepath

    def browse_light_watermark(self):
        try:
            filepath = self.browse_watermark()
            self.watermark_light_filepath = filepath
            filename = os.path.basename(filepath)
            self.light_status.configure(text=filename)
        except NotSupportedFileFormatException as exc:
            self.watermark_light_filepath = DEFAULT_LIGHT_WATERMARK
            self.light_status.configure(text="Default")
            self.error_callback(str(exc))

    def browse_dark_watermark(self):
        try:
            filepath = self.browse_watermark()
            self.watermark_dark_filepath = filepath
            filename = os.path.basename(filepath)
            self.dark_status.configure(text=filename)
        except NotSupportedFileFormatException as exc:
            self.watermark_dark_filepath = DEFAULT_DARK_WATERMARK
            self.dark_status.configure(text="Default")
            self.error_callback(str(exc))
