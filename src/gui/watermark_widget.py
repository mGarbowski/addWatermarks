import os.path
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Frame, Label, Button
from typing import Callable

from core.directory_processors import DirectoryProcessor


class WatermarkWidget(Frame):
    """
    UI component for selecting a watermark file to apply to photos
    """

    def __init__(self, container: Frame, label: str, default_filepath: str, error_callback: Callable):
        """
        :param container: parent UI component
        :param label: label text to display
        :param default_filepath: path to the default watermark file
        :param error_callback: callback function to display error messages
        """

        super().__init__(container)

        self.__default_filepath = default_filepath
        self.__filepath = default_filepath
        self.__error_callback = error_callback

        self.__label = Label(self, text=label, width=10)
        self.__status = Label(self, text="Default", width=15)
        self.__button = Button(self, text="Change", command=self.__browse_watermark)

        self.__label.grid(row=0, column=0, sticky=tk.W)
        self.__status.grid(row=0, column=1)
        self.__button.grid(row=0, column=2, sticky=tk.E)

    def __browse_watermark(self) -> None:
        """
        Open a system dialog for the user to select the file
        and validate whether it is of a supported type
        """

        filepath = filedialog.askopenfilename()
        _, extension = os.path.splitext(filepath)
        if extension not in DirectoryProcessor.SUPPORTED_WATERMARK_FILE_FORMATS:
            self.__filepath = self.__default_filepath
            self.__status.configure(text="Default")
            self.__error_callback("Not supported filetype, watermarks must be of type(s): "  
                                  f"{''.join(DirectoryProcessor.SUPPORTED_WATERMARK_FILE_FORMATS)}")
            # TODO: raise Exception instead
        else:
            self.__filepath = filepath
            filename = os.path.basename(filepath)
            self.__status.configure(text=filename)
            self.__error_callback("")  # Clear error display

    def get_watermark_filepath(self) -> str:
        """
        Get selected watermark's filepath

        :return: filepath to the selected watermark file
        """

        return self.__filepath
