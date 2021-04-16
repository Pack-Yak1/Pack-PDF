from tkinter import (
    Tk, filedialog, messagebox, font, StringVar, Frame, Label, Entry, Button
)
from img2pdf import convert as jpgConvert
from img2pdf import ImageOpenError
from PIL import Image, ImageOps
from traceback import format_exc
from logging import basicConfig, error
from os import getcwd, mkdir, path, remove, system
from addressHolder import *
from subprocess import Popen
from json import dump, load
from interface import *

HOME_DIR = getcwd()
try:
    mkdir(path.join(HOME_DIR, "temp"))
except FileExistsError:
    pass
finally:
    TEMP_DIR = path.join(HOME_DIR, "temp")
LOG_FILE = path.join(HOME_DIR, "logs.txt")
CONFIG_FILE = path.join(HOME_DIR, "config.json")


# Supported image formats (besides .jpg)
SUPPORTED_FORMATS = [".png", ".jpeg", ".bmp"]


# Main window
root = Tk()
root.geometry("500x150")
root.resizable(0, 0)
root.title("JPG to PDF Converter by Pack Yak1")
root.config(background=BACKGROUND_COLOR)


# Get config data to initialize backend
try:
    with open(CONFIG_FILE, "r") as f:
        config = load(f)
        data = AddressHolder(config)
except FileNotFoundError:
    with open(CONFIG_FILE, "w") as f:
        dump(DEFAULT_CONFIG, f)
        data = AddressHolder(DEFAULT_CONFIG)


# Display strings & functions
SUCCESS_TITLE = "Success!"
SAVED_CONFIG_MESSAGE = "Default settings successfully updated"


# Success message upon converting/combining a pdf
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


def displayInfo(t, m, p):
    messagebox.showinfo(title=t, message=m, parent=p)


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
        displayInfo(NO_SELECTION_TITLE, NO_SELECTION_PROMPT, root)
        return True
    # No save path selected
    elif data.savePath == "":
        displayInfo(NO_DEST_TITLE, NO_DEST_PROMPT, root)
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


# Button functions


# TODO: reordering selected images
# TODO: readme info (supported image types, default ordering)
# TODO: support more image types
# TODO: combine pdf
def convert():
    if not checkEmptyInputs():
        try:
            convertImagesToJpg()
            with open(data.savePath, "wb") as f:
                f.write(jpgConvert(data.imageNames))
                data.lastOutputAddress = data.savePath
                displayInfo(SUCCESS_TITLE, SUCCESS_MESSAGE(), root)
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
        system("notepad %s" % LOG_FILE)
    except Exception:
        unknownErrorProtocol()


def stringVarOf(o):
    output = StringVar()
    if type(o) is type(""):
        output.set(o)
        return output
    else:
        raise ValueError(
            "Attempted to call stringVarOf on non-string object"
        )


def saveConfig(fields, topLevel):
    try:
        for key in fields:
            value = fields.get(key).get()
            if value != "":  # only update if user selects a path
                data.config[key] = value
        with open(CONFIG_FILE, "w") as f:
            dump(data.config, f)
            displayInfo(SUCCESS_TITLE, SAVED_CONFIG_MESSAGE, topLevel)
            topLevel.destroy()
    except Exception:
        unknownErrorProtocol()


def changeDefaults():
    defaultsWindow = defaultFrameNoResize("500x150", "Change default settings")

    # StringVars for fields containing config settings
    currentWorkspace = data.config.get("default workspace")
    text1Ptr = stringVarOf(currentWorkspace)
    currentDest = data.config.get("default destination")
    text2Ptr = stringVarOf(currentDest)

    fields = {"default workspace": text1Ptr,
              "default destination": text2Ptr}

    # TODO: abstractify button commands, maybe make an array of stringvar ptrs
    # First row (workspace label, field, button)
    (workspaceLabel, workspaceText, browseButton3) = defaultRow(
        "Default Workspace:", text1Ptr, "Browse",
        lambda: text1Ptr.set(filedialog.askdirectory(
            initialdir=currentWorkspace,
            parent=defaultsWindow
        )), defaultsWindow)
    workspaceLabel.grid(row=1, column=0, pady=10, padx=5, columnspan=2)
    workspaceText.grid(row=1, column=2, pady=10, padx=5, columnspan=2)
    browseButton3.grid(row=1, column=4, pady=4, padx=1)

    # Second row (destination label, field, button)
    (destLabel, destText, browseButton4) = defaultRow(
        "Default Save Address:", text2Ptr, "Browse",
        lambda: text2Ptr.set(filedialog.askdirectory(
            initialdir=currentDest,
            parent=defaultsWindow
        )), defaultsWindow)
    destLabel.grid(row=2, column=0, pady=5, padx=5, columnspan=2)
    destText.grid(row=2, column=2, pady=5, padx=5, columnspan=2)
    browseButton4.grid(row=2, column=4, pady=4, padx=1)
    defaultsWindow.lift()

    # Third row (Save button)
    saveButton = defaultButton("Save",
                               lambda: saveConfig(fields, defaultsWindow),
                               defaultsWindow)
    saveButton.grid(row=3, column=2, pady=5, padx=3)
    cancelButton = defaultButton("Cancel", defaultsWindow.destroy,
                                 defaultsWindow)
    cancelButton.grid(row=3, column=4, pady=5, padx=3)


def widgets():
    # First row (Browse label, field, button)
    (linkLabel, linkText, browseButton1) = defaultRow(
        "Images selected:", data.nameDisplay, "Browse", data.updateImageNames,
        root)
    linkLabel.grid(row=1, column=0, pady=10, padx=5, columnspan=2)
    linkText.grid(row=1, column=2, pady=10, padx=5, columnspan=2)
    browseButton1.grid(row=1, column=4, pady=4, padx=1)

    # Second row (Save as label, field, button)
    (destinationLabel, destinationText, browseButton2) = defaultRow(
        "Save to:", data.saveDisplay, "Browse", data.updateSavePath,
        root)
    destinationLabel.grid(row=2, column=0, pady=5, padx=5, columnspan=2)
    destinationText.grid(row=2, column=2, pady=5, padx=5, columnspan=2)
    browseButton2.grid(row=2, column=4, pady=4, padx=1)

    # Third row (Convert button)
    convertButton = defaultButton("Convert", convert, root)
    convertButton.grid(row=3, column=2, pady=5, padx=3)

    # Fourth row(open output, defaults, log button)
    lastOutputButton = defaultButton("Open output", openLastOutput, root)
    lastOutputButton.grid(row=4, column=2, pady=5, padx=3)

    defaultsButton = defaultButton("Defaults", changeDefaults, root)
    defaultsButton.grid(row=4, column=3, pady=5, padx=3)

    logFileButton = defaultButton("Open logs", openLogs, root)
    logFileButton.grid(row=4, column=4, pady=5, padx=3)


widgets()
root.mainloop()
