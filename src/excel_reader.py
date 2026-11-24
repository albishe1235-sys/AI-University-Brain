
from openpyxl import load_workbook

def read_excel(file_path):
    workbook = load_workbook(file_path, data_only=True)

    text = ""

    for sheet in workbook.worksheets:
        text += "Sheet: " + sheet.title + "\n"

        for row in sheet.iter_rows(values_only=True):
            text += " | ".join(
                str(cell) if cell is not None else ""
                for cell in row
            ) + "\n"

    return text
