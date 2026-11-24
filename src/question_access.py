
from search_engine import ranked_search
from user_manager import authorize_session


def ask_question_for_user(token, question, lectures):

    user = authorize_session(
        token,
        "/content/AI_University_Brain/data/users.json",
        "ask_question"
    )

    available = lectures

    if user["role"] == "student":
        available = [
            lecture for lecture in lectures
            if lecture["department"] == user["department"]
            and lecture["stage"] == user["stage"]
        ]

    elif user["role"] == "doctor":
        available = [
            lecture for lecture in lectures
            if lecture["doctor"] == user["username"]
        ]

    results = ranked_search(question, available)

    if not results:
        return "No matching information found."

    best_result = results[0]
    lecture = best_result["lecture"]

    return {
        "answer": lecture["content"],
        "university": lecture["university"],
        "doctor": lecture["doctor"],
        "department": lecture["department"],
        "stage": lecture["stage"],
        "subject": lecture["subject"],
        "source": lecture["file_name"],
        "page_number": lecture.get("page_number"),
        "score": best_result["score"]
    }
