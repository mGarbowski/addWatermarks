import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Label

from gui.corner_menu import CornerConfigMenu
from gui.proportion_entry import ProportionEntry


class ConfigMenu(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)

        self.dark_label = Label(self, text='Dark:')
        self.dark_label.grid(row=0, column=0, sticky=tk.W)
        # TODO:

        self.light_label = Label(self, text='Light:')
        self.light_label.grid(row=1, column=0, sticky=tk.W)
        # TODO:

        self.width_label = Label(self, text="Width:")
        self.height_label = Label(self, text="Height:")
        self.opacity_label = Label(self, text="Opacity:")
        self.width_entry = ProportionEntry(self, default_value=0.15)
        self.height_entry = ProportionEntry(self, default_value=0.15)
        self.opacity_entry = ProportionEntry(self, default_value=0.5)

        self.width_label.grid(row=2, column=0, sticky=tk.W)
        self.height_label.grid(row=3, column=0, sticky=tk.W)
        self.opacity_label.grid(row=4, column=0, sticky=tk.W)
        self.width_entry.grid(row=2, column=1, sticky=tk.E)
        self.height_entry.grid(row=3, column=1, sticky=tk.E)
        self.opacity_entry.grid(row=4, column=1, sticky=tk.E)

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
