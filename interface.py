from tkinter import Frame, Label, Entry, Button, Tk, Toplevel, messagebox

# Colors
LABEL_COLOR = "#d8bc94"
LABEL_TEXT_COLOR = "#000000"
LABEL_BORDER_COLOR = "#98846c"
BUTTON_COLOR = "#685444"
BUTTON_TEXT_COLOR = "#FFFFFF"
BACKGROUND_COLOR = "#e8dccc"
FIELD_COLOR = "#f0ece4"
FIELD_TEXT_COLOR = "#000000"

# Display strings & functions
SUCCESS_TITLE = "Success!"
SAVED_CONFIG_MESSAGE = "Default settings successfully updated"
RESET_CONFIG_MESSAGE = "Setting successfully reset"
RESET_ALL_CONFIG_MESSAGE = "All settings successfully reset to default values"


# Success message upon converting/combining a pdf
def SUCCESS_MESSAGE(data):
    return "%d images successfully converted to PDF at %s" % (
        len(data.imageNames), data.savePath
    )


RESET_ALL_TITLE = "Reset all defaults"
RESET_ALL_MESSAGE = "Are you sure you wish to reset all configurations to default settings?"

CORRUPT_CONFIG_TITLE = "Config file improperly formatted"
CORRUPT_CONFIG_MESSAGE = "The config file is improperly formatted and needs to be reset to continue. Your settings will be reset if you continue"

NO_SELECTION_TITLE = "No images selected for conversion"
NO_SELECTION_PROMPT = "Please select images before clicking Convert."

NO_DEST_TITLE = "No save path selected"
NO_DEST_PROMPT = "Please select a destination to save pdf to."

FILE_IN_USE_TITLE = "File is currently in use"
FILE_IN_USE_ERROR = "Your pdf was not converted because it is currently in use. Try closing it before overwriting."

INVALID_FILE_TYPE_TITLE = "Invalid file(s) selected"
INVALID_FILE_TYPE_ERROR = "Check that only .png .jpg or .bmp images have been selected."

UNKNOWN_ERROR_TITLE = "An unknown error has occured"
UNKNOWN_ERROR = "Your last action may not have been executed correctly. Please check the log file and report it at: https://github.com/Pack-Yak1/image-to-pdf/issues"

NO_LOG_TITLE = "No logs to show"
NO_LOG_MSG = "No errors occured so far, so no logs have been recorded."


# Default widget/frame construction functions
def defaultFrameNoResize(geom, title):
    output = Toplevel()
    output.geometry(geom)
    output.resizable(0, 0)
    output.title(title)
    output.config(background=BACKGROUND_COLOR)
    return output


def defaultLabel(label, frame):
    # Creates a label within a border with color = LABEL_BORDER_COLOR and return
    # the border it is packed into
    border = Frame(frame, bg=LABEL_BORDER_COLOR)
    label = Label(border, text=label, bg=LABEL_COLOR, fg=LABEL_TEXT_COLOR,
                  width=20)
    label.pack(padx=1, pady=1)
    return border


def defaultField(textVar, frame):
    return Entry(frame, width=40, textvariable=textVar, bg=FIELD_COLOR,
                 fg=FIELD_TEXT_COLOR, relief="sunken")


def defaultButton(label, func, frame):
    return Button(frame, text=label, command=func, width=10, bg=BUTTON_COLOR,
                  fg=BUTTON_TEXT_COLOR)


# Consists of a label, a text field, and a button
def defaultRow(rowNumber, label, field, buttonLabel, buttonFunc, frame):
    label = defaultLabel(label, frame)
    label.grid(row=rowNumber, column=0, pady=10, padx=5, columnspan=2)

    field = defaultField(field, frame)
    field.grid(row=rowNumber, column=2, pady=10, padx=5, columnspan=2)

    button = defaultButton(buttonLabel, buttonFunc, frame)
    button.grid(row=rowNumber, column=4, pady=4, padx=1)


def default2BtnRow(
        rowNumber, label, field, b1Label, b1Fn, b2Label, b2Fn, frame):
    defaultRow(rowNumber, label, field, b1Label, b1Fn, frame)
    button2 = defaultButton(b2Label, b2Fn, frame)
    button2.grid(row=rowNumber, column=5, pady=4, padx=1)


def displayInfo(t, m, p):
    messagebox.showinfo(title=t, message=m, parent=p)


def displayWarning(t, m, p):
    messagebox.showwarning(title=t, message=m, parent=p)


def notifyError(t, m, p):
    messagebox.showerror(title=t, message=m, parent=p)


def displayOkCancel(t, m, p):
    return messagebox.askokcancel(title=t, message=m, parent=p)
