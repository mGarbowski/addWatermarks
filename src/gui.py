import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo
from tkinter.ttk import Label, Entry

from src.watermarking import Corner


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

        self.browse_btn = ttk.Button(self, text='Browse', command=self.browse_directories)
        self.browse_btn.grid(row=1, column=0, sticky=tk.W)

        self.directory = tk.StringVar()
        self.directory.set('directory containing photos')
        self.directory_info = ttk.Entry(self, textvariable=self.directory)
        self.directory_info.grid(row=1, column=1, columnspan=3, sticky=tk.W)

        self.add_btn = ttk.Button(self, text='ADD', command=lambda: self.watermark_photos)
        self.add_btn.grid(row=1, column=3)

        self.config_menu = ConfigMenu(self)
        self.config_menu.grid(row=3, column=0)

    def browse_directories(self):
        photos_directory = filedialog.askdirectory()
        self.directory.set(photos_directory)

    def watermark_photos(self):
        pass


class ConfigMenu(ttk.Frame):
    default_dark_watermark = 'watermark-dark.png'
    default_white_watermark = './watermark-light.png'

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

        try:
            proportion = float(proportion_text)
            if 1 < proportion < 100:
                proportion = proportion / 100

            if not (0.0 < proportion <= 1.0):
                raise ValueError('Must be between 1 and 100 or 0 and 1')

            return proportion

        except ValueError as err:
            showinfo(title='Incorrect value', message=str(err))


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


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
