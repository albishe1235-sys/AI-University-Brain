
from search_engine import ranked_search

def answer_question(question, lectures):

    results = ranked_search(question, lectures)

    if not results:
        return "No matching information found."

    best_result = results[0]
    best = best_result["lecture"]

    return {
        "answer": best["content"],
        "subject": best["subject"],
        "source": best["file_name"],
        "page_number": best.get("page_number"),
        "score": best_result["score"]
    }
