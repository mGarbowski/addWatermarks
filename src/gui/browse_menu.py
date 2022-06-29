import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Frame, Label, Button, Entry


class BrowseMenu(Frame):

    def __init__(self, container, add_callback):
        super().__init__(container)

        self.browse_btn = Button(self, text='Browse', command=self.browse_directories)
        self.browse_btn.grid(row=1, column=0, sticky=tk.E)

        self.directory = tk.StringVar()
        self.directory.set('directory containing photos')
        self.directory_info = Entry(self, textvariable=self.directory, width=100)
        self.directory_info.grid(row=1, column=1, sticky=tk.W)

        self.add_btn = Button(self, text='ADD', command=lambda: add_callback())
        self.add_btn.grid(row=1, column=3)

    def browse_directories(self):
        photos_directory = filedialog.askdirectory()
        self.directory.set(photos_directory)

    def get_directory(self):
        return self.directory.get()
