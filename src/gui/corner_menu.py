import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Label

from core.watermarking import Corner


class CornerConfigMenu(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.upper_left = tk.BooleanVar()
        self.upper_right = tk.BooleanVar()
        self.bottom_left = tk.BooleanVar()
        self.bottom_right = tk.BooleanVar()

        self.upper_left_label = Label(self, text='Upper left')
        self.upper_left_label.grid(row=0, column=0, sticky=tk.W)
        self.upper_left_check = ttk.Checkbutton(self, offvalue=False, onvalue=True, variable=self.upper_left)
        self.upper_left_check.grid(row=0, column=1)
        self.upper_left_check.selection_clear()

        self.upper_right_label = Label(self, text='Upper right')
        self.upper_right_label.grid(row=0, column=3, sticky=tk.E)
        self.upper_right_check = ttk.Checkbutton(self, offvalue=False, onvalue=True, variable=self.upper_right)
        self.upper_right_check.grid(row=0, column=2)

        self.bottom_left_label = Label(self, text='Bottom left')
        self.bottom_left_label.grid(row=1, column=0, sticky=tk.W)
        self.bottom_left_check = ttk.Checkbutton(self, offvalue=False, onvalue=True, variable=self.bottom_left)
        self.bottom_left_check.grid(row=1, column=1)

        self.bottom_right_label = Label(self, text='Bottom right')
        self.bottom_right_label.grid(row=1, column=3, sticky=tk.E)
        self.bottom_right_check = ttk.Checkbutton(self, offvalue=False, onvalue=True, variable=self.bottom_right)
        self.bottom_right_check.grid(row=1, column=2)

    def get_corners(self):
        corners = []
        if self.upper_left.get():
            corners.append(Corner.UPPER_LEFT)
        if self.upper_right.get():
            corners.append(Corner.UPPER_RIGHT)
        if self.bottom_left.get():
            corners.append(Corner.LOWER_LEFT)
        if self.bottom_right.get():
            corners.append(Corner.LOWER_RIGHT)

        return corners
