import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Frame, Button, Entry
from typing import Callable


class BrowseMenu(Frame):
    """
    UI component for selecting a directory with photos to process
    and a button initiating processing TODO: refactor - single responsibility
    """

    def __init__(self, container: Frame, add_callback: Callable):
        """
        :param container: parent widget
        :param add_callback: callback function, called on button press
        """

        super().__init__(container)

        self.browse_btn = Button(self, text='Browse', command=self.browse_directories)
        self.browse_btn.grid(row=1, column=0, sticky=tk.E)

        self.directory = tk.StringVar()
        self.directory.set('directory containing photos')
        self.directory_info = Entry(self, textvariable=self.directory, width=100)
        self.directory_info.grid(row=1, column=1, sticky=tk.W)

        self.add_btn = Button(self, text='ADD', command=lambda: add_callback())
        self.add_btn.grid(row=1, column=3)

    def browse_directories(self) -> None:
        """
        Open a system pop-up window to select a folder
        """

        photos_directory = filedialog.askdirectory()
        self.directory.set(photos_directory)

    def get_directory(self) -> str:
        """
        Get the selected directory's path

        :return: path to the selected directory
        """
        return self.directory.get()
