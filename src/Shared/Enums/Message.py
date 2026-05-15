from enum import StrEnum


class Message(StrEnum):

    CREATING_CYCLE = "Creating a new cycle..."
    FINISH_PROCCESS = "Process finished successfully"
    MISSING_REQUIRED_FIELDS = "Missing required fields"
    INVALID_DATES = "Provided dates are not valid"
    DEDUCTIONS_UPLOADED = "Deductions uploaded successfully"
    DEDUCTIONS_EXIST = "Cycle already have deductions"
    NO_DEDUCTIONS_EDITED_MSG = "No deductions were edited"
    INVALID_FILE_STRUCTURE = "Invalid file structure"
    NO_COMPENSATIONS_EDITED = "No compensations were edited"
