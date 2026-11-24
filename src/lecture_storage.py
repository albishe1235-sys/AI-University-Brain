
import json
import os

def save_lectures(new_lectures, storage_path):

    if os.path.exists(storage_path):
        with open(storage_path, "r", encoding="utf-8") as file:
            lectures = json.load(file)
    else:
        lectures = []

    existing = {}

    for index, item in enumerate(lectures):
        key = (
            item["file_name"],
            item["subject"],
            item["stage"],
            item["chunk_id"]
        )
        existing[key] = index

    added = 0
    updated = 0

    for lecture in new_lectures:

        key = (
            lecture["file_name"],
            lecture["subject"],
            lecture["stage"],
            lecture["chunk_id"]
        )

        if key in existing:
            index = existing[key]
            lectures[index].update(lecture)
            updated += 1
        else:
            lectures.append(lecture)
            existing[key] = len(lectures) - 1
            added += 1

    with open(storage_path, "w", encoding="utf-8") as file:
        json.dump(lectures, file, ensure_ascii=False, indent=4)

    return added, len(lectures), updated


def load_lectures(storage_path):

    if not os.path.exists(storage_path):
        return []

    with open(storage_path, "r", encoding="utf-8") as file:
        return json.load(file)
