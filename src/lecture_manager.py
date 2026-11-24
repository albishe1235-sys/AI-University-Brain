
import os

from file_reader import read_file
from pdf_reader import read_pdf
from metadata_validator import validate_metadata
from file_validator import validate_file


def split_text(text, chunk_size=100, overlap=20):

    words = text.split()
    chunks = []

    step = chunk_size - overlap

    for i in range(0, len(words), step):

        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def process_lecture(file_path, metadata):

    validate_file(file_path)

    missing = validate_metadata(metadata)

    if missing:
        raise ValueError("Missing information: " + str(missing))

    processed = []

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":

        pages = read_pdf(file_path)

        for page in pages:

            chunks = split_text(page["content"])

            for chunk in chunks:

                processed.append({
                    "chunk_id": len(processed) + 1,
                    "page_number": page["page_number"],
                    "content": chunk,
                    "university": metadata["university"],
                    "department": metadata["department"],
                    "stage": metadata["stage"],
                    "subject": metadata["subject"],
                    "doctor": metadata["doctor"],
                    "file_name": os.path.basename(file_path)
                })

    else:

        text = read_file(file_path)
        chunks = split_text(text)

        for chunk in chunks:

            processed.append({
                "chunk_id": len(processed) + 1,
                "page_number": None,
                "content": chunk,
                "university": metadata["university"],
                "department": metadata["department"],
                "stage": metadata["stage"],
                "subject": metadata["subject"],
                "doctor": metadata["doctor"],
                "file_name": os.path.basename(file_path)
            })

    return processed
