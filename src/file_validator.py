
import os

def validate_file(file_path):

    if not os.path.isfile(file_path):
        raise FileNotFoundError("File does not exist!")

    allowed_extensions = [
        ".pdf", ".docx", ".pptx", ".xlsx", ".txt"
    ]

    extension = os.path.splitext(file_path)[1].lower()

    if extension not in allowed_extensions:
        raise ValueError("File type not supported!")

    return True
