from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
import img2pdf
import PIL.Image

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
        self.imageNames = list(tkinter.filedialog.askopenfilenames())
        self.nameDisplay.set(str(self.imageNames)[1:-1].replace("'", ""))
        self.imageNames

    def updateSavePath(self):
        self.savePath = tkinter.filedialog.asksaveasfilename()
        self.saveDisplay.set(self.savePath)


data = AddressHolder()


def chooseFiles():
    data.updateImageNames()


def chooseSavePath():
    data.updateSavePath()


def convert():
    if data.imageNames == []:
        tkinter.messagebox.showinfo(title="No images selected for conversion",
                                    message="Please select images before clicking Convert.")

    elif data.savePath == "":
        tkinter.messagebox.showinfo(title="No save path selected",
                                    message="Please select a destination to save pdf to.")

    else:
        for i in range(len(data.imageNames)):
            address = data.imageNames[i]
            if ".png" in address:
                with PIL.Image.open(address) as image:
                    jpgvers = PIL.Image.new("RGB", image.size, (255, 255, 255))
                    jpgvers.paste(image, image)
                    jpgName = address[:-4] + ".jpg"
                    jpgvers.save(jpgName, quality=95)
                    data.imageNames[i] = jpgName

        try:
            with open(data.savePath, "wb") as f:
                f.write(img2pdf.convert(data.imageNames))
                tkinter.messagebox.showinfo(
                    title="Success!", message="%d images successfully converted to PDF at %s" % (len(data.imageNames), data.savePath))
        except PermissionError:
            tkinter.messagebox.showerror(title="File is currently in use",
                                         message="Your pdf was not converted because it is currently in use. Try closing it before overwriting.")


def Widgets():
    linkLabel = Label(root, text="Images selected:",
                      bg="#E8D579", width=20)
    linkLabel.grid(row=1, column=0, pady=10, padx=5)

    linkText = Entry(root, width=40, textvariable=data.nameDisplay)
    linkText.grid(row=1, column=1, pady=10, padx=5)

    browseButton1 = Button(root, text="Browse",
                           command=chooseFiles, width=10, bg="#05E8E0")
    browseButton1.grid(row=1, column=2, pady=4, padx=1)

    destinationLabel = Label(
        root, text="Save to :", bg="#E8D579", width=20)
    destinationLabel.grid(row=2, column=0, pady=5, padx=5)

    destinationText = Entry(root, width=40, textvariable=data.saveDisplay)
    destinationText.grid(row=2, column=1, pady=5, padx=5)

    browseButton2 = Button(root, text="Browse",
                           command=chooseSavePath, width=10, bg="#05E8E0")
    browseButton2.grid(row=2, column=2, pady=4, padx=1)

    convertButton = Button(root, text="Convert",
                           command=convert, width=10, bg="#05E8E0")
    convertButton.grid(row=3, column=1, pady=5, padx=3)


Widgets()
root.mainloop()
