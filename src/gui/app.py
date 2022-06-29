import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Label

from core.directory_processors import FlatDirectoryProcessor
from core.exceptions import NoneSelectedException
from gui.browse_menu import BrowseMenu
from gui.config_menu import ConfigMenu


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

        self.browse_menu = BrowseMenu(self, self.watermark_photos)
        self.browse_menu.grid(row=2, columnspan=2)

        self.config_menu = ConfigMenu(self, error_callback=self.set_error_message)
        self.config_menu.grid(row=3, column=0, sticky=tk.W, padx=25)

        self.status_label = Label(self, text="", font=('Helvetica', 12))
        self.status_label.grid(row=4, pady=20)

        style = ttk.Style()
        style.configure("Green.TLabel", foreground="green")
        style.configure("Error.TLabel", foreground="red")

    def watermark_photos(self):
        try:
            processor = FlatDirectoryProcessor(
                dark_watermark_filepath=self.config_menu.get_dark_watermark_filepath(),
                light_watermark_filepath=self.config_menu.get_light_watermark_filepath(),
                max_width_proportion=self.config_menu.get_width(),
                max_height_proportion=self.config_menu.get_height(),
                opacity=self.config_menu.get_opacity(),
                corners=self.config_menu.get_corners()
            )
            processor.handle_directory(self.browse_menu.get_directory())
            self.set_success_message("Watermarks added successfully")
        except OSError as err:
            self.set_error_message(str(err))
        except ValueError as err:
            self.set_error_message(str(err))
        except NoneSelectedException as err:
            self.set_error_message(str(err))

    def set_success_message(self, message: str):
        self.status_label.configure(text=message)
        self.status_label.configure(style="Green.TLabel")

    def set_error_message(self, message: str):
        self.status_label.configure(text=message)
        self.status_label.configure(style="Error.TLabel")
