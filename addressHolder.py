from tkinter import StringVar, filedialog


# Stores the selected images, save path, and string variables to display in
# fields.
class AddressHolder:
    def __init__(self):
        self.imageNames = []
        self.savePath = ""
        self.nameDisplay = StringVar()
        self.saveDisplay = StringVar()
        self.createdFiles = set()
        self.lastOutputAddress = None

    def updateImageNames(self):
        self.imageNames = list(
            filedialog.askopenfilenames(
                title="Select images to convert to PDF",
            )
        )
        self.nameDisplay.set(str(self.imageNames)[1:-1].replace("'", ""))
        self.imageNames

    def updateSavePath(self):
        self.savePath = filedialog.asksaveasfilename(
            defaultextension='.pdf',
            title="Save PDF to:",
            filetypes=[("PDF", "*.pdf")]
        )
        self.saveDisplay.set(self.savePath)

    def reset(self):
        self.imageNames = []
        self.savePath = ""
        self.nameDisplay.set("")
        self.saveDisplay.set("")
        self.createdFiles.clear()
