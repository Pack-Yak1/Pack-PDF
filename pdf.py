from tkinter import (
    Tk, filedialog, messagebox, font, StringVar, Frame, Label, Entry, Button
)
from img2pdf import convert as jpgConvert
from img2pdf import ImageOpenError
from PIL import Image, ImageOps
from traceback import format_exc
from logging import basicConfig, error
from os import getcwd, mkdir, path, remove, system
from addressHolder import AddressHolder
from subprocess import Popen

HOME_DIR = getcwd()
try:
    mkdir(path.join(HOME_DIR, "temp"))
except FileExistsError:
    pass
finally:
    TEMP_DIR = path.join(HOME_DIR, "temp")
LOG_FILE = path.join(HOME_DIR, "logs.txt")

# Supported image formats (besides .jpg)
SUPPORTED_FORMATS = [".png", ".jpeg", ".bmp"]


# Colors
LABEL_COLOR = "#d8bc94"
LABEL_TEXT_COLOR = "#000000"
LABEL_BORDER_COLOR = "#98846c"
BUTTON_COLOR = "#685444"
BUTTON_TEXT_COLOR = "#FFFFFF"
BACKGROUND_COLOR = "#e8dccc"
FIELD_COLOR = "#f0ece4"
FIELD_TEXT_COLOR = "#000000"


# Main window
root = Tk()
root.geometry("500x120")
root.resizable(0, 0)
root.title("JPG to PDF Converter by Pack Yak1")
root.config(background=BACKGROUND_COLOR)


# Backend initialization
data = AddressHolder()


# Display strings & functions
SUCCESS_TITLE = "Success!"


def SUCCESS_MESSAGE():
    return "%d images successfully converted to PDF at %s" % (
        len(data.imageNames), data.savePath
    )


NO_SELECTION_TITLE = "No images selected for conversion"
NO_SELECTION_PROMPT = "Please select images before clicking Convert."

NO_DEST_TITLE = "No save path selected"
NO_DEST_PROMPT = "Please select a destination to save pdf to."

FILE_IN_USE_TITLE = "File is currently in use"
FILE_IN_USE_ERROR = "Your pdf was not converted because it is currently in use. Try closing it before overwriting."

INVALID_FILE_TYPE_TITLE = "Invalid file(s) selected"
INVALID_FILE_TYPE_ERROR = "Check that only .png .jpg or .bmp images have been selected."

UNKNOWN_ERROR_TITLE = "An unknown error has occured"
UNKNOWN_ERROR = "Your pdf may not have been produced correctly. Please check the log file and report it at: https://github.com/Pack-Yak1/image-to-pdf/issues"


def displayInfo(t, m):
    messagebox.showinfo(title=t, message=m)


def notifyError(t, m):
    messagebox.showerror(title=t, message=m)


# Converts a supported image at [address] to a jpg image with the same name and
# location. Returns the address of the jpg image created.
def imgToJpg(address):
    with Image.open(address).convert("RGBA") as image:
        index = len(data.createdFiles)
        image = ImageOps.exif_transpose(image)  # check for rotation
        jpgvers = Image.new("RGB", image.size, (255, 255, 255))
        jpgvers.paste(image, image)
        jpgName = path.join(TEMP_DIR, "%d.jpg" % index)
        jpgvers.save(jpgName, quality=95)
        return jpgName


# Checks if user attempted to convert without selecting files and destination
def checkEmptyInputs():
    # No files selected for conversion
    if data.imageNames == []:
        displayInfo(NO_SELECTION_TITLE, NO_SELECTION_PROMPT)
        return True
    # No save path selected
    elif data.savePath == "":
        displayInfo(NO_DEST_TITLE, NO_DEST_PROMPT)
        return True
    else:
        return False


# Check for data.imageNames for supported extensions and convert to jpg in temp
# directory. Replaces non-jpg version of image in data.imageNames and updates
# data.createdFiles to include produced jpg address
def convertImagesToJpg():
    for i in range(len(data.imageNames)):
        address = data.imageNames[i]
        extensionIndex = address.rfind(".")
        extension = address[extensionIndex:]
        if extension != ".jpg" and extension in SUPPORTED_FORMATS:
            jpgName = imgToJpg(address)
            data.imageNames[i] = jpgName
            data.createdFiles.add(jpgName)


def unknownErrorProtocol():
    basicConfig(filename=LOG_FILE, filemode="w")
    error(format_exc())
    notifyError(UNKNOWN_ERROR_TITLE, UNKNOWN_ERROR)


# TODO: reordering selected images
# TODO: readme info (supported image types, default ordering)
# TODO: support more image types
# TODO: combine pdf
# TODO: default directories
def convert():
    if not checkEmptyInputs():
        try:
            convertImagesToJpg()
            with open(data.savePath, "wb") as f:
                f.write(jpgConvert(data.imageNames))
                data.lastOutputAddress = data.savePath
                displayInfo(SUCCESS_TITLE, SUCCESS_MESSAGE())
        except PermissionError:
            # File is in use
            notifyError(FILE_IN_USE_TITLE, FILE_IN_USE_ERROR)
        except ImageOpenError:
            # Non supported image filetypes were selected
            notifyError(INVALID_FILE_TYPE_TITLE, INVALID_FILE_TYPE_ERROR)
        except Exception:
            # Any other error
            unknownErrorProtocol()
        finally:
            for path in data.createdFiles:
                remove(path)
            data.reset()


def openLastOutput():
    if data.lastOutputAddress != None:
        try:
            system(data.lastOutputAddress)
        except Exception:
            unknownErrorProtocol()


def openLogs():
    try:
        system("explorer %s" % HOME_DIR)
    except Exception:
        unknownErrorProtocol()


# Default widget construction functions


def defaultLabel(label):
    # Creates a label within a border with color = LABEL_BORDER_COLOR and return
    # the border it is packed into
    border = Frame(root, bg=LABEL_BORDER_COLOR)
    label = Label(border, text=label, bg=LABEL_COLOR, fg=LABEL_TEXT_COLOR,
                  width=20)
    label.pack(padx=1, pady=1)
    return border


def defaultField(textVar):
    return Entry(root, width=40, textvariable=textVar, bg=FIELD_COLOR,
                 fg=FIELD_TEXT_COLOR, relief="sunken")


def defaultButton(label, func):
    return Button(root, text=label, command=func, width=10, bg=BUTTON_COLOR,
                  fg=BUTTON_TEXT_COLOR)


def widgets():
    # First row (Browse label, field, button)
    linkLabel = defaultLabel("Images selected:")
    linkLabel.grid(row=1, column=0, pady=10, padx=5, columnspan=2)

    linkText = defaultField(data.nameDisplay)
    linkText.grid(row=1, column=2, pady=10, padx=5, columnspan=2)

    browseButton1 = defaultButton("Browse", data.updateImageNames)
    browseButton1.grid(row=1, column=4, pady=4, padx=1)

    # Second row (Save as label, field, button)
    destinationLabel = defaultLabel("Save to :")
    destinationLabel.grid(row=2, column=0, pady=5, padx=5, columnspan=2)

    destinationText = defaultField(data.saveDisplay)
    destinationText.grid(row=2, column=2, pady=5, padx=5, columnspan=2)

    browseButton2 = defaultButton("Browse", data.updateSavePath)
    browseButton2.grid(row=2, column=4, pady=4, padx=1)

    # Third row (Convert button, open output button)
    convertButton = defaultButton("Convert", convert)
    convertButton.grid(row=3, column=2, pady=5, padx=3)

    lastOutputButton = defaultButton("Open output", openLastOutput)
    lastOutputButton.grid(row=3, column=3, pady=5, padx=3)

    logFileButton = defaultButton("Open logs", openLogs)
    logFileButton.grid(row=3, column=4, pady=5, padx=3)


widgets()
root.mainloop()
