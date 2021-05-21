from tkinter import Frame, Label, Entry, Button, Tk, Toplevel, messagebox

# Colors
_LABEL_COLOR = "#d8bc94"
_LABEL_TEXT_COLOR = "#000000"
_LABEL_BORDER_COLOR = "#98846c"
_BUTTON_COLOR = "#685444"
_BUTTON_TEXT_COLOR = "#FFFFFF"
BACKGROUND_COLOR = "#e8dccc"
_FIELD_COLOR = "#f0ece4"
_FIELD_TEXT_COLOR = "#000000"


# Default widget/frame construction functions
def defaultFrameNoResize(output, geom, title):
    output.geometry(geom)
    output.resizable(0, 0)
    output.title(title)
    output.config(background=BACKGROUND_COLOR)
    return output


def _defaultLabel(label, frame):
    # Creates a label within a border with color = LABEL_BORDER_COLOR and return
    # the border it is packed into
    border = Frame(frame, bg=_LABEL_BORDER_COLOR)
    label = Label(border, text=label, bg=_LABEL_COLOR, fg=_LABEL_TEXT_COLOR,
                  width=15)
    label.pack(padx=1, pady=1)
    return border


def _defaultField(textVar, frame):
    return Entry(frame, width=35, textvariable=textVar, bg=_FIELD_COLOR,
                 fg=_FIELD_TEXT_COLOR, relief="sunken")


def defaultButton(label, func, frame):
    return Button(frame, text=label, command=func, width=10, bg=_BUTTON_COLOR,
                  fg=_BUTTON_TEXT_COLOR)


# Consists of a label, a text field, and a button
def defaultRow(rowNumber, label, field, buttonLabel, buttonFunc, frame):
    label = _defaultLabel(label, frame)
    label.grid(row=rowNumber, column=0, pady=10, padx=5, columnspan=2)

    field = _defaultField(field, frame)
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


def displayError(t, m, p):
    messagebox.showerror(title=t, message=m, parent=p)


def displayOkCancel(t, m, p):
    return messagebox.askokcancel(title=t, message=m, parent=p)
