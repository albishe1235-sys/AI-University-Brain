
import os

from pdf_reader import read_pdf
from word_reader import read_word
from ppt_reader import read_ppt
from excel_reader import read_excel
from txt_reader import read_txt

def read_file(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    readers = {
        ".pdf": read_pdf,
        ".docx": read_word,
        ".pptx": read_ppt,
        ".xlsx": read_excel,
        ".txt": read_txt
    }

    if extension not in readers:
        raise ValueError("File type not supported")

    return readers[extension](file_path)
