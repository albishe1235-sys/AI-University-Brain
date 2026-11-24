
from lecture_manager import process_lecture
from lecture_storage import save_lectures

def add_lecture(file_path, metadata, database_path):

    processed = process_lecture(file_path, metadata)

    added, total, updated = save_lectures(
        processed,
        database_path
    )

    return {
        "added": added,
        "updated": updated,
        "total": total,
        "subject": metadata["subject"]
    }
