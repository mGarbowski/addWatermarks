import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter.ttk import Label, Entry

from .corner_menu import CornerConfigMenu


class ConfigMenu(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)

        self.dark_label = Label(self, text='Dark:')
        self.dark_label.grid(row=0, column=0, sticky=tk.W)

        self.light_label = Label(self, text='Light:')
        self.light_label.grid(row=1, column=0, sticky=tk.W)

        self._width = tk.StringVar()
        self.width_label = Label(self, text='Width:')
        self.width_label.grid(row=2, column=0, sticky=tk.W)
        self.width_entry = Entry(self, textvariable=self._width)
        self.width_entry.grid(row=2, column=1)

        self._height = tk.StringVar()
        self.height_label = Label(self, text='Height:')
        self.height_label.grid(row=3, column=0, sticky=tk.W)
        self.height_entry = Entry(self, textvariable=self._height)
        self.height_entry.grid(row=3, column=1)

        self._opacity = tk.StringVar()
        self.opacity_label = Label(self, text='Opacity:')
        self.opacity_label.grid(row=4, column=0, sticky=tk.W)
        self.opacity_entry = Entry(self, textvariable=self._opacity)
        self.opacity_entry.grid(row=4, column=1)

        self.corner_config_menu = CornerConfigMenu(self)
        self.corner_config_menu.grid(row=5, columnspan=3)

    def get_corners(self):
        return self.corner_config_menu.get_corners()

    def get_width(self):
        return self._validate_proportion(self._height)

    def get_height(self):
        return self._validate_proportion(self._height)

    def get_opacity(self):
        return self._validate_proportion(self._opacity)

    @staticmethod
    def _validate_proportion(value):
        proportion_text = value.get()
        proportion_text = proportion_text.strip()
        if ',' in proportion_text:
            proportion_text = proportion_text.replace(',', '.')

        proportion = float(proportion_text)

        if not (0.0 < proportion <= 1.0):
            raise ValueError('Must be between 0 and 1')

        return proportion
