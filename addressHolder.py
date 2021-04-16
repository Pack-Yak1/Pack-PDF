from tkinter import StringVar, filedialog


# Default config
DEFAULT_CONFIG = {"default workspace": "", "default destination": ""}


# Stores the selected images, save path, and string variables to display in
# fields.
class AddressHolder:
    def __init__(self, config):
        self.imageNames = []
        self.savePath = ""
        self.nameDisplay = StringVar()
        self.saveDisplay = StringVar()
        self.createdFiles = set()
        self.lastOutputAddress = None
        self.config = config

    def updateImageNames(self):
        self.imageNames = list(
            filedialog.askopenfilenames(
                title="Select images to convert to PDF",
                initialdir=self.config.get("default workspace")
            )
        )
        self.nameDisplay.set(str(self.imageNames)[1:-1].replace("'", ""))
        self.imageNames

    def updateSavePath(self):
        self.savePath = filedialog.asksaveasfilename(
            defaultextension='.pdf',
            title="Save PDF to:",
            filetypes=[("PDF", "*.pdf")],
            initialdir=self.config.get("default destination")
        )
        self.saveDisplay.set(self.savePath)

    def reset(self):
        self.imageNames = []
        self.savePath = ""
        self.nameDisplay.set("")
        self.saveDisplay.set("")
        self.createdFiles.clear()
