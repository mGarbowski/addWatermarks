import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter.ttk import Label

from core.directory_processors import FlatDirectoryProcessor
from resources.watermarks import DEFAULT_DARK_WATERMARK, DEFAULT_LIGHT_WATERMARK
from .config_menu import ConfigMenu


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry('800x600+10+10')
        self.title('Watermarking tool')

        self.main_body = MainBody(self)
        self.main_body.pack(expand=True, fill='both')


class MainBody(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        self.main_label = Label(self, text="Add watermarks", font=('Helvetica', 30))
        self.main_label.grid(row=0, column=0)

        self.browse_btn = ttk.Button(self, text='Browse', command=self.browse_directories)
        self.browse_btn.grid(row=1, column=0, sticky=tk.W)

        self.directory = tk.StringVar()
        self.directory.set('directory containing photos')
        self.directory_info = ttk.Entry(self, textvariable=self.directory)
        self.directory_info.grid(row=1, column=1, columnspan=3, sticky=tk.W)

        self.add_btn = ttk.Button(self, text='ADD', command=lambda: self.watermark_photos())
        self.add_btn.grid(row=1, column=3)

        self.config_menu = ConfigMenu(self)
        self.config_menu.grid(row=3, column=0)

    def browse_directories(self):
        photos_directory = filedialog.askdirectory()
        self.directory.set(photos_directory)

    def watermark_photos(self):
        processor = FlatDirectoryProcessor(
            dark_watermark_filepath=DEFAULT_DARK_WATERMARK,
            light_watermark_filepath=DEFAULT_LIGHT_WATERMARK,
            max_width_proportion=self.config_menu.get_width(),
            max_height_proportion=self.config_menu.get_height(),
            opacity=self.config_menu.get_opacity(),
            corners=self.config_menu.get_corners()
        )

        processor.handle_directory(self.directory.get())
