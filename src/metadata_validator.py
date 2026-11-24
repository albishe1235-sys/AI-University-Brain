
def validate_metadata(metadata):

    required_fields = [
        "university",
        "department",
        "stage",
        "subject",
        "doctor",
        "file_name"
    ]

    missing_fields = []

    for field in required_fields:
        if not metadata.get(field):
            missing_fields.append(field)

    return missing_fields
