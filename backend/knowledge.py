import json
import os
import re


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "aishani.json")


def load_knowledge():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


knowledge = load_knowledge()


STOP_WORDS = {
    "what", "where", "when", "who", "why", "how",
    "does", "did", "has", "have", "had",
    "with", "about", "tell", "give", "show",
    "aishani", "her", "she", "the", "and",
    "for", "from", "that", "this", "was",
    "were", "are", "is", "me"
}


def get_search_words(question):
    question = question.lower()

    # Keep letters, numbers, + and #
    question = re.sub(r"[^a-z0-9+#\s]", "", question)

    words = question.split()

    return [
        word for word in words
        if len(word) > 1 and word not in STOP_WORDS
    ]


def search_value(value, words, path="", results=None):

    if results is None:
        results = []

    if isinstance(value, str):

        text = value.lower()
        score = 0

        for word in words:

            if text == word:
                score += 5

            elif word in text:
                score += 2

        if score > 0:

            if "experience" in path:
                score += 2

            if "projects" in path:
                score += 1

            if "skills" in path:
                score += 1

            results.append({
                "text": value,
                "path": path,
                "score": score
            })


    elif isinstance(value, list):

        for index, item in enumerate(value):
            search_value(
                item,
                words,
                f"{path}[{index}]",
                results
            )


    elif isinstance(value, dict):

        for key, item in value.items():
            search_value(
                item,
                words,
                f"{path}.{key}",
                results
            )


    return results


def search_knowledge(question, limit=5):

    words = get_search_words(question)

    results = search_value(
        knowledge,
        words
    )

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:limit]


if __name__ == "__main__":

    question = "Does Aishani know C++?"

    results = search_knowledge(question)

    print("Question:", question)

    print("\nSearch results:")

    for result in results:
        print(
            result["score"],
            "-",
            result["text"]
        )