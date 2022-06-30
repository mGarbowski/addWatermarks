import tkinter as tk
from tkinter.ttk import Label, Checkbutton, Frame

from core.exceptions import NoneSelectedException
from core.watermarking import Corner


class CornerConfigMenu(Frame):
    """
    UI component with checkboxes for selecting corners where watermarks can be placed
    """

    def __init__(self, container: Frame):
        """
        :param container: parent component
        """

        super().__init__(container)
        self.upper_left = tk.BooleanVar()
        self.upper_right = tk.BooleanVar()
        self.bottom_left = tk.BooleanVar()
        self.bottom_right = tk.BooleanVar()

        # Some default behaviour
        self.upper_right.set(True)
        self.upper_left.set(True)

        self.upper_left_label = Label(self, text='Upper left')
        self.upper_right_label = Label(self, text='Upper right')
        self.bottom_left_label = Label(self, text='Bottom left')
        self.bottom_right_label = Label(self, text='Bottom right')

        self.upper_left_check = Checkbutton(self, offvalue=False, onvalue=True, variable=self.upper_left)
        self.upper_right_check = Checkbutton(self, offvalue=False, onvalue=True, variable=self.upper_right)
        self.bottom_left_check = Checkbutton(self, offvalue=False, onvalue=True, variable=self.bottom_left)
        self.bottom_right_check = Checkbutton(self, offvalue=False, onvalue=True, variable=self.bottom_right)

        self.upper_left_label.grid(row=0, column=0, sticky=tk.W)
        self.upper_right_label.grid(row=0, column=3, sticky=tk.E)
        self.bottom_left_label.grid(row=1, column=0, sticky=tk.W)
        self.bottom_right_label.grid(row=1, column=3, sticky=tk.E)

        self.upper_left_check.grid(row=0, column=1)
        self.upper_right_check.grid(row=0, column=2)
        self.bottom_left_check.grid(row=1, column=1)
        self.bottom_right_check.grid(row=1, column=2)

    def get_corners(self) -> list[Corner]:
        """
        Get selected corners

        :return: list of selected corners
        :raises NoneSelectedException: when no corners are selected
        """
        corners = []
        if self.upper_left.get():
            corners.append(Corner.UPPER_LEFT)
        if self.upper_right.get():
            corners.append(Corner.UPPER_RIGHT)
        if self.bottom_left.get():
            corners.append(Corner.LOWER_LEFT)
        if self.bottom_right.get():
            corners.append(Corner.LOWER_RIGHT)

        if len(corners) == 0:
            raise NoneSelectedException("Please select at least one corner")

        return corners
