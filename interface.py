from tkinter import Frame, Label, Entry, Button, Tk, Toplevel

# Colors
LABEL_COLOR = "#d8bc94"
LABEL_TEXT_COLOR = "#000000"
LABEL_BORDER_COLOR = "#98846c"
BUTTON_COLOR = "#685444"
BUTTON_TEXT_COLOR = "#FFFFFF"
BACKGROUND_COLOR = "#e8dccc"
FIELD_COLOR = "#f0ece4"
FIELD_TEXT_COLOR = "#000000"

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
def defaultRow(label, field, buttonLabel, buttonFunc, frame):
    label = defaultLabel(label, frame)
    field = defaultField(field, frame)
    button = defaultButton(buttonLabel, buttonFunc, frame)
    return(label, field, button)
