
import re

def normalize_text(text):
    return re.findall(r'\w+', text.lower())


def ranked_search(keyword, lectures):

    stop_words = {
        "what", "is", "the", "a", "an", "of", "in",
        "are", "and", "to", "for", "how"
    }

    keywords = set(normalize_text(keyword)) - stop_words

    if not keywords:
        return []

    results = []

    for lecture in lectures:

        content_words = set(
            normalize_text(lecture["content"])
        )

        subject_words = set(
            normalize_text(lecture["subject"])
        )

        content_matches = keywords & content_words
        subject_matches = keywords & subject_words

        matched_words = content_matches | subject_matches

        score = (
            len(content_matches)
            + (2 * len(subject_matches))
        )

        if len(matched_words) >= min(2, len(keywords)):

            results.append({
                "lecture": lecture,
                "score": score
            })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results
