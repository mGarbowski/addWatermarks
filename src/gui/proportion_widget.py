import tkinter as tk
from tkinter.ttk import Frame, Label, Entry


class ProportionWidget(Frame):
    """
    UI component for selecting proportion values, between 0 and 1
    """

    def __init__(self, container: Frame, label: str, default_value: float):
        """
        :param container: parent UI component
        :param label: label text to display
        :param default_value: default value of the entry field
        """
        super().__init__(container)

        self.__value = tk.StringVar()
        self.__value.set(str(default_value))

        self.label = Label(self, text=label, width=10)
        self.entry = Entry(self, textvariable=self.__value, width=6)

        self.label.grid(row=0, column=0, sticky=tk.W)
        self.entry.grid(row=0, column=1, columnspan=2, sticky=tk.E)

    @staticmethod
    def __validate_proportion(proportion_text: str) -> float:
        """
        Validate whether selected value is a valid proportion
        Handles both commas and decimal points

        :param proportion_text: text representation of the proportion
        :return: proportion value if valid
        :raises InvalidProportionException: if the user provided an illegal value
        """

        proportion_text = proportion_text.strip()
        if ',' in proportion_text:
            proportion_text = proportion_text.replace(',', '.')

        try:
            proportion = float(proportion_text)

            if not (0.0 < proportion <= 1.0):
                raise InvalidProportionException('Must be between 0 and 1')

            return proportion

        except ValueError:
            raise InvalidProportionException("Invalid value, must be between 0 and 1")

    def get_value(self) -> float:
        """
        Get the value selected by user.
        Validates input.

        :return: value selected by user
        :raises InvalidProportionException: if the user provided an illegal value
        """

        return self.__validate_proportion(self.__value.get())


class InvalidProportionException(Exception):
    """Raised if the user provides an invalid value for a proportion"""

    pass
