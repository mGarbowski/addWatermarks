import tkinter as tk
from tkinter.ttk import Frame, Label, Entry


class ProportionEntry(Frame):

    def __init__(self, container, default_value: float):
        super().__init__(container)
        self.__value = tk.StringVar()
        self.__value.set(str(default_value))

        self.entry = Entry(self, textvariable=self.__value)
        self.entry.grid(row=0, column=1, sticky=tk.E)

    @staticmethod
    def __validate_proportion(value):
        proportion_text = value.get()
        proportion_text = proportion_text.strip()
        if ',' in proportion_text:
            proportion_text = proportion_text.replace(',', '.')

        proportion = float(proportion_text)

        if not (0.0 < proportion <= 1.0):
            raise ValueError('Must be between 0 and 1')

        return proportion

    def get_value(self):
        return self.__validate_proportion(self.__value)
