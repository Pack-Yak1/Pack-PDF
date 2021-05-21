WINDOW_TITLE = "JPG to PDF Converter by Pack Yak1"
WINDOW_SIZE = "437x290"

# Display strings & functions
SUCCESS_TITLE = "Success!"
SAVED_CONFIG_MESSAGE = "Default settings successfully updated"
RESET_CONFIG_MESSAGE = "Setting successfully reset"
RESET_ALL_CONFIG_MESSAGE = "All settings successfully reset to default values"


# Success message upon converting/combining a pdf
def CONVERT_SUCCESS_MESSAGE(data):
    return "%d images successfully converted to PDF at %s" % (
        len(data.convertNames), data.convertDest
    )


def COMBINE_SUCCESS_MESSAGE(data):
    return "%d PDFs successfully combined and saved to %s" % (
        len(data.combineNames), data.combineDest
    )


RESET_ALL_TITLE = "Reset all defaults"
RESET_ALL_MESSAGE = "Are you sure you wish to reset all configurations to default settings?"

CORRUPT_CONFIG_TITLE = "Config file improperly formatted"
CORRUPT_CONFIG_MESSAGE = "The config file is improperly formatted and needs to be reset to continue. Your settings will be reset if you continue"

NO_CONVERT_SELECTION_TITLE = "No images selected for conversion"
NO_CONVERT_SELECTION_PROMPT = "Please select images before clicking Convert."

NO_COMBINE_SELECTION_TITLE = "No PDFs selected for combining"
NO_COMBINE_SELECTION_PROMPT = "Please select PDFs "

NO_DEST_TITLE = "No save path selected"
NO_DEST_PROMPT = "Please select a destination to save pdf to."

FILE_IN_USE_TITLE = "File is currently in use"
FILE_IN_USE_ERROR = "Your pdf was not converted because it is currently in use. Try closing it before overwriting."

INVALID_FILE_TYPE_TITLE = "Invalid file(s) selected"
CONVERT_INVALID_FILE_TYPE_ERROR = "Check that only .png .jpg or .bmp images have been selected."
COMBINE_INVALID_FILE_TYPE_ERROR = "Check that only PDFs were selected for combining."

UNKNOWN_ERROR_TITLE = "An unknown error has occured"
UNKNOWN_ERROR = "Your last action may not have been executed correctly. Please check the log file and report it at: https://github.com/Pack-Yak1/image-to-pdf/issues"

NO_LOG_TITLE = "No logs to show"
NO_LOG_MSG = "No errors occured so far, so no logs have been recorded."

STRINGVAR_GENERATION_TYPE_ERROR = "Attempted to call stringVarOf on non-string object"
