from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
import img2pdf
import PIL.Image


# Main window
root = Tk()
root.geometry("500x120")
root.resizable(0, 0)
root.title("JPG to PDF Converter by Pack Yak1")
root.config(background="#000000")


class AddressHolder:
    def __init__(self):
        self.imageNames = []
        self.savePath = ""
        self.nameDisplay = StringVar()
        self.saveDisplay = StringVar()

    def updateImageNames(self):
        self.imageNames = list(
            tkinter.filedialog.askopenfilenames(
                title="Select images to convert to PDF",
            )
        )
        self.nameDisplay.set(str(self.imageNames)[1:-1].replace("'", ""))
        self.imageNames

    def updateSavePath(self):
        self.savePath = tkinter.filedialog.asksaveasfilename(
            defaultextension='.pdf',
            title="Save PDF to:",
            filetypes=[("PDF", "*.pdf")]
        )
        self.saveDisplay.set(self.savePath)


# Converts a png image at [address] to a jpg image with the same name and
# location. Returns the address of the jpg image created.
def pngToJpg(address):
    with PIL.Image.open(address) as image:
        jpgvers = PIL.Image.new("RGB", image.size, (255, 255, 255))
        jpgvers.paste(image, image)
        jpgName = address[:-4] + ".jpg"
        jpgvers.save(jpgName, quality=95)
        return jpgName


data = AddressHolder()


# Display strings
SUCCESS_TITLE = "Success!"
SUCCESS_MESSAGE = "%d images successfully converted to PDF at %s" % (
    len(data.imageNames), data.savePath)

NO_SELECTION_TITLE = "No images selected for conversion"
NO_SELECTION_PROMPT = "Please select images before clicking Convert."

NO_DEST_TITLE = "No save path selected"
NO_DEST_PROMPT = "Please select a destination to save pdf to."

FILE_IN_USE_TITLE = "File is currently in use"
FILE_IN_USE_ERROR = "Your pdf was not converted because it is currently in use. Try closing it before overwriting."

INVALID_FILE_TYPE_TITLE = "Invalid file(s) selected"
INVALID_FILE_TYPE_ERROR = "Check that only .png and .jpg images have been selected."


def convert():
    # No files selected for conversion
    if data.imageNames == []:
        tkinter.messagebox.showinfo(
            title=NO_SELECTION_TITLE,
            message=NO_SELECTION_PROMPT
        )

    # No save path selected
    elif data.savePath == "":
        tkinter.messagebox.showinfo(
            title=NO_DEST_TITLE,
            message=NO_DEST_PROMPT
        )

    else:
        # Check for png extensions, automatically convert to jpg
        for i in range(len(data.imageNames)):
            address = data.imageNames[i]
            if ".png" in address:
                data.imageNames[i] = pngToJpg(address)
        # TODO: Prompt user about which jpgs were created, ask if delete

        # TODO: Non png exception handling
        try:
            with open(data.savePath, "wb") as f:
                f.write(img2pdf.convert(data.imageNames))
                tkinter.messagebox.showinfo(
                    title=SUCCESS_TITLE,
                    message=SUCCESS_MESSAGE
                )
        # File is in use
        except PermissionError:
            tkinter.messagebox.showerror(
                title=FILE_IN_USE_TITLE,
                message=FILE_IN_USE_ERROR
            )
        except img2pdf.ImageOpenError:
            tkinter.messagebox.showerror(
                title=INVALID_FILE_TYPE_TITLE,
                message=INVALID_FILE_TYPE_ERROR
            )


def Widgets():
    linkLabel = Label(root, text="Images selected:",
                      bg="#E8D579", width=20)
    linkLabel.grid(row=1, column=0, pady=10, padx=5)

    linkText = Entry(root, width=40, textvariable=data.nameDisplay)
    linkText.grid(row=1, column=1, pady=10, padx=5)

    browseButton1 = Button(root, text="Browse",
                           command=data.updateImageNames,
                           width=10, bg="#05E8E0")
    browseButton1.grid(row=1, column=2, pady=4, padx=1)

    destinationLabel = Label(
        root, text="Save to :", bg="#E8D579", width=20)
    destinationLabel.grid(row=2, column=0, pady=5, padx=5)

    destinationText = Entry(root, width=40, textvariable=data.saveDisplay)
    destinationText.grid(row=2, column=1, pady=5, padx=5)

    browseButton2 = Button(root, text="Browse",
                           command=data.updateSavePath, width=10, bg="#05E8E0")
    browseButton2.grid(row=2, column=2, pady=4, padx=1)

    convertButton = Button(root, text="Convert",
                           command=convert, width=10, bg="#05E8E0")
    convertButton.grid(row=3, column=1, pady=5, padx=3)


Widgets()
root.mainloop()
