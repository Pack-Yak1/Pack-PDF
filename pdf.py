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
from subprocess import *
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
root.geometry("500x290")
root.resizable(0, 0)
root.title("JPG to PDF Converter by Pack Yak1")
root.config(background=BACKGROUND_COLOR)


# Default config
DEFAULT_CONFIG = {"default workspace": "", "default destination": ""}


# Get config data to initialize backend
try:
    with open(CONFIG_FILE, "r") as f:
        config = load(f)
        if DEFAULT_CONFIG.keys() != config.keys():
            resetCheck = displayOkCancel(
                CORRUPT_CONFIG_TITLE, CORRUPT_CONFIG_MESSAGE, root)
            if resetCheck:
                raise FileNotFoundError
            else:
                root.destroy()
                exit(0)
        data = AddressHolder(config)
except FileNotFoundError:
    with open(CONFIG_FILE, "w") as f:
        dump(DEFAULT_CONFIG, f)
        data = AddressHolder(DEFAULT_CONFIG)


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
def checkConvertEmptyInputs():
    # No files selected for conversion
    if data.convertNames == []:
        displayInfo(NO_CONVERT_SELECTION_TITLE,
                    NO_CONVERT_SELECTION_PROMPT, root)
        return True
    # No save path selected
    elif data.convertDest == "":
        displayInfo(NO_DEST_TITLE, NO_DEST_PROMPT, root)
        return True
    else:
        return False


def checkCombineEmptyInputs():
    # No PDFs selected for combining
    if data.combineNames == []:
        displayInfo(NO_COMBINE_SELECTION_TITLE,
                    NO_COMBINE_SELECTION_PROMPT, root)
        return True
    # No save path selected
    elif data.convertDest == "":
        displayInfo(NO_DEST_TITLE, NO_DEST_PROMPT, root)
        return True
    else:
        return False


def combinePDFS():
    pass


# Check for data.convertNames for supported extensions and convert to jpg in temp
# directory. Replaces non-jpg version of image in data.convertNames and updates
# data.createdFiles to include produced jpg address
def convertImagesToJpg():
    for i in range(len(data.convertNames)):
        address = data.convertNames[i]
        extensionIndex = address.rfind(".")
        extension = address[extensionIndex:]
        if extension != ".jpg" and extension in SUPPORTED_FORMATS:
            jpgName = imgToJpg(address)
            data.convertNames[i] = jpgName
            data.createdFiles.add(jpgName)


def unknownErrorProtocol(parent):
    with open(LOG_FILE, "w") as f:
        f.write("")
    basicConfig(filename=LOG_FILE, filemode="w")
    error(format_exc())
    notifyError(UNKNOWN_ERROR_TITLE, UNKNOWN_ERROR, parent)


# Button functions


# TODO: reordering selected images
# TODO: help button (supported image types, default ordering)
# TODO: support more image types
# TODO: combine pdf
# TODO: reorder pages (take last file as input button optional)
def convert():
    if not checkConvertEmptyInputs():
        try:
            convertImagesToJpg()
            with open(data.convertDest, "wb") as f:
                f.write(jpgConvert(data.imageNames))
                data.lastOutputAddress = data.convertDest
                displayInfo(SUCCESS_TITLE, SUCCESS_MESSAGE(data), root)
        except PermissionError:
            # File is in use
            notifyError(FILE_IN_USE_TITLE, FILE_IN_USE_ERROR, root)
        except ImageOpenError:
            # Non supported image filetypes were selected
            notifyError(INVALID_FILE_TYPE_TITLE, INVALID_FILE_TYPE_ERROR, root)
        except Exception:
            # Any other error
            unknownErrorProtocol(root)
        finally:
            for path in data.createdFiles:
                remove(path)
            data.resetConvert()


def combine():
    if not checkCombineEmptyInputs():
        try:
            combinePDFs()
            with open(data.combineDest, "wb") as f:
                pass
        except PermissionError:
            # File is in use
            notifyError(FILE_IN_USE_TITLE, FILE_IN_USE_ERROR, root)
        except ImageOpenError:  # TODO: change this to non pdf selected error
            # Non supported image filetypes were selected
            notifyError(INVALID_FILE_TYPE_TITLE, INVALID_FILE_TYPE_ERROR, root)
        except Exception:
            # Any other error
            unknownErrorProtocol(root)
        finally:
            data.resetCombine()


# Code from https://stackoverflow.com/questions/7006238/how-do-i-hide-the-consol
# e-when-i-use-os-system-or-subprocess-call/7006424#7006424
def noCmdSystemCall(command):
    si = STARTUPINFO()
    si.dwFlags |= STARTF_USESHOWWINDOW
    # si.wShowWindow = subprocess.SW_HIDE # default
    Popen([command], shell=True, startupinfo=si)


def openLastOutput():
    if data.lastOutputAddress != None:
        try:
            noCmdSystemCall(data.lastOutputAddress)
        except Exception:
            unknownErrorProtocol(root)


def openLogs():
    try:
        if (path.exists(LOG_FILE)):
            noCmdSystemCall(LOG_FILE)
        else:
            displayInfo(NO_LOG_TITLE, NO_LOG_MSG, root)
    except Exception:
        unknownErrorProtocol(root)


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
        unknownErrorProtocol(topLevel)


def resetConfigField(txtPtr, key, value, topLevel):
    try:
        txtPtr.set("")
        data.config[key] = value
        with open(CONFIG_FILE, "w") as f:
            dump(data.config, f)
            displayInfo(SUCCESS_TITLE, RESET_CONFIG_MESSAGE, topLevel)
    except Exception:
        unknownErrorProtocol(topLevel)


def resetAllConfigs(topLevel, fields):
    try:
        confirm = displayOkCancel(RESET_ALL_TITLE, RESET_ALL_MESSAGE, topLevel)
        if confirm:
            for key in fields:
                fields[key].set("")  # reset displayed text of all fields
                data.config[key] = ""  # reset actual setting
            with open(CONFIG_FILE, "w") as f:
                dump(data.config, f)
                displayInfo(SUCCESS_TITLE, RESET_ALL_CONFIG_MESSAGE, topLevel)
        else:
            return
    except Exception:
        unknownErrorProtocol(topLevel)


def changeDefaults():
    # StringVars for fields containing config settings
    currentWorkspace = data.config.get("default workspace")
    text1Ptr = stringVarOf(currentWorkspace)
    currentDest = data.config.get("default destination")
    text2Ptr = stringVarOf(currentDest)

    fields = {"default workspace": text1Ptr,
              "default destination": text2Ptr}

    defaultsWindow = defaultFrameNoResize("585x160", "Change default settings")
    rowNumber = 0

    # First row (workspace label, field, button)
    default2BtnRow(
        rowNumber,
        "Default Workspace:", text1Ptr,
        "Browse", lambda: text1Ptr.set(filedialog.askdirectory(
            initialdir=currentWorkspace,
            parent=defaultsWindow
        )),
        "Reset", lambda: resetConfigField(
            text1Ptr, "default workspace", "", defaultsWindow
        ),
        defaultsWindow
    )
    rowNumber += 1

    # Second row (destination label, field, button)
    default2BtnRow(
        rowNumber,
        "Default Save Address:", text2Ptr,
        "Browse", lambda: text2Ptr.set(filedialog.askdirectory(
            initialdir=currentDest,
            parent=defaultsWindow
        )),
        "Reset", lambda: resetConfigField(
            text2Ptr, "default destination", "", defaultsWindow
        ),
        defaultsWindow)
    rowNumber += 1

    # Penultimate row (Save button)
    saveButton = defaultButton("Save",
                               lambda: saveConfig(fields, defaultsWindow),
                               defaultsWindow)
    saveButton.grid(row=3, column=3, pady=5, padx=3)
    # rowNumber += 1

    # Fourth row (Reset all, cancel)
    resetAllButton = defaultButton(
        "Reset All", lambda: resetAllConfigs(
            defaultsWindow, fields
        ), defaultsWindow
    )
    resetAllButton.grid(row=4, column=4, pady=5, padx=3)
    cancelButton = defaultButton("Cancel", defaultsWindow.destroy,
                                 defaultsWindow)
    cancelButton.grid(row=4, column=5, pady=5, padx=3)

    defaultsWindow.lift()


def widgets():
    rowNumber = 0
    # First row (Browse label, field, button)
    defaultRow(
        rowNumber,
        "Images selected:", data.convertNameDisplay,
        "Browse", data.updateConvertNames,
        root
    )
    rowNumber += 1

    # Second row (Save as label, field, button)
    defaultRow(
        rowNumber,
        "Save to:", data.convertSaveDisplay,
        "Browse", data.updateConvertDest,
        root
    )
    rowNumber += 1

    # Third row (Convert button)
    convertButton = defaultButton("Convert", convert, root)
    convertButton.grid(row=rowNumber, column=2, pady=5, padx=3)
    rowNumber += 1

    # Fourth row (Select PDFs to combine)
    defaultRow(
        rowNumber,
        "PDFs selected:", data.combineNameDisplay,
        "Browse", data.updateCombineNames,
        root
    )
    rowNumber += 1

    # Fifth row (Save as label, field, button)
    defaultRow(
        rowNumber,
        "Save to:", data.combineSaveDisplay,
        "Browse", data.updateCombineDest,
        root
    )
    rowNumber += 1

    # Sixth row (Combine button)
    convertButton = defaultButton("Combine", combine, root)
    convertButton.grid(row=rowNumber, column=2, pady=5, padx=3)
    rowNumber += 1

    # Last row(open output, defaults, log button)
    lastOutputButton = defaultButton("Open output", openLastOutput, root)
    lastOutputButton.grid(row=rowNumber, column=2, pady=5, padx=3)

    defaultsButton = defaultButton("Defaults", changeDefaults, root)
    defaultsButton.grid(row=rowNumber, column=3, pady=5, padx=3)

    logFileButton = defaultButton("Open logs", openLogs, root)
    logFileButton.grid(row=rowNumber, column=4, pady=5, padx=3)


widgets()
root.mainloop()
