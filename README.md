# CLI and GUI utility for automatic photo watermarking
NOTE: This is and early build, more functionality will be added in the future, some functionalities may not work properly

## Capabilities
The application chooses the most uniform corner out of those specified by user and then chooses 
either dark or light variant of the watermark based on the average brightness in that corner.

It **does not** modify any files in the provided folder and places all watermarked photos in a subdirectory. 

Choose custom watermarks via the GUI application or by modifying contents of `src\resources\watermarks`

## Technologies
* Written in Python
* Uses [Pillow](https://python-pillow.org/) for manipulating images
* GUI built with [tkinter](https://docs.python.org/3/library/tkinter.html)

## Installation
* Install Python3 and pip, consider following this [useful guide](https://realpython.com/installing-python/)
* Install dependencies by changing into the project directory eg. `cd C:\Users\<username>\Desktop\addWatermarks`
* Run `pip install -r requirements.txt` to install the dependencies

## Usage
* Use a more user-friendly GUI version of the app by
  * Entering the source folder eg. `cd C:\Users\<username>\Desktop\addWatermarks\src`
  * And running `python main.py`
* CLI version is also available
  * From the source folder (see above) run `python cli.py -f <path-to-the-folder-with-photos>` 
  * Or simply run `python cli.py -h` to display the help page
