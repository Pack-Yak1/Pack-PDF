from tkinter import StringVar, filedialog


# Stores the selected images, save path, and string variables to display in
# fields.
class AddressHolder:
    def __init__(self, config):
        # Shared across all features
        self.createdFiles = set()
        self.lastOutputAddress = None
        self.config = config

        # Used by image to pdf
        self.convertNames = []
        self.convertDest = ""
        self.convertNameDisplay = StringVar()
        self.convertSaveDisplay = StringVar()

        # Used by combine pdf
        self.combineNames = []
        self.combineDest = ""
        self.combineNameDisplay = StringVar()
        self.combineSaveDisplay = StringVar()

    # Updates the text displayed in images selected for conversion field
    def updateConvertNames(self):
        self.convertNames = list(
            filedialog.askopenfilenames(
                title="Select images to convert to PDF",
                initialdir=self.config.get("default workspace")
            )
        )
        self.convertNameDisplay.set(str(self.convertNames)[
                                    1:-1].replace("'", ""))

    # Updates the text displayed as save destination for image to pdf
    def updateConvertDest(self):
        self.convertDest = filedialog.asksaveasfilename(
            defaultextension='.pdf',
            title="Save PDF as:",
            filetypes=[("PDF", "*.pdf")],
            initialdir=self.config.get("default destination")
        )
        self.convertSaveDisplay.set(self.convertDest)

    # Reset the convert image to pdf fields
    def resetConvert(self):
        self.convertNames = []
        self.convertDest = ""
        self.convertNameDisplay.set("")
        self.convertSaveDisplay.set("")
        self.createdFiles.clear()

    def updateCombineNames(self):
        self.combineNames = list(
            filedialog.askopenfilenames(
                title="Select PDFs to combine",
                initialdir=self.config.get("default workspace"),
                defaultextension=".pdf"
            )
        )
        self.combineNameDisplay.set(
            str(self.combineNames)[1:-1].replace("'", "")
        )

    def updateCombineDest(self):
        self.combineDest = filedialog.asksaveasfilename(
            defaultextension='.pdf',
            title="Save combined PDF as:",
            filetypes=[("PDF", "*.pdf")],
            initialdir=self.config.get("default destination")
        )
        self.combineSaveDisplay.set(self.combineDest)
