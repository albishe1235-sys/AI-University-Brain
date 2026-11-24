from lecture_pipeline import add_lecture
from user_manager import authorize_session


def upload_lecture_for_user(
    token,
    file_path,
    metadata,
    users_database_path,
    lectures_database_path
):

    user = authorize_session(
        token,
        users_database_path,
        "upload_lecture"
    )

    if user["role"] == "doctor":
        if metadata["doctor"] != user["username"]:
            raise PermissionError(
                "Doctors can only upload lectures under their own name."
            )

    return add_lecture(
        file_path,
        metadata,
        lectures_database_path
    )
