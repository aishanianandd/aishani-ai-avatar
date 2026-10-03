from flask import Flask, request, jsonify
from flask_cors import CORS
from knowledge import search_knowledge

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "Aishani AI backend is running!"
    })


def generate_answer(question, results):
    q = question.lower()

    if not results:
        return (
            "I don't have enough information about Aishani "
            "to answer that question yet."
        )

    # C++
    if "c++" in q or "cpp" in q:
        return (
            "Yes! Aishani has experience with C++. "
            "She developed an interactive text-based mystery game in C++ "
            "as part of her CS 100 course, where she worked with branching "
            "storylines, user input handling, modular functions, and "
            "multiple possible outcomes."
        )

    # Python
    if "python" in q:
        return (
            "Yes! Aishani has experience with Python, including using it "
            "for backend development and AI-related projects. She has also "
            "worked with Flask while building her AI portfolio assistant."
        )

    # AI / artificial intelligence
    if (
        "artificial intelligence" in q
        or " ai " in f" {q} "
        or "machine learning" in q
        or "generative ai" in q
    ):
        return (
            "Aishani has experience and exposure to AI through research "
            "and technical projects. Her experience includes generative AI, "
            "natural language processing concepts, large language models, "
            "and building AI-powered backend systems."
        )

    # Projects
    if (
        "project" in q
        or "built" in q
        or "build" in q
        or "game" in q
    ):
        return (
            "Aishani has worked on several technical projects. One of her "
            "projects is an interactive text-based mystery game developed "
            "in C++ for CS 100. She has also worked on AI-related projects "
            "and backend systems."
        )

    # Education
    if (
        "education" in q
        or "school" in q
        or "college" in q
        or "university" in q
        or "study" in q
        or "major" in q
    ):
        return (
            "Aishani is a third-year Computational Cognitive Science "
            "student at UC Davis. Her interests include artificial "
            "intelligence, machine learning, human-centered technology, "
            "and software development."
        )

    # Skills
    if (
        "skill" in q
        or "programming language" in q
        or "coding" in q
        or "technical" in q
    ):
        return (
            "Aishani has experience with programming and software "
            "development, including C++ and Python. She has also worked "
            "with GitHub, backend development, AI concepts, and "
            "collaborative software projects."
        )

    # Experience
    if (
        "experience" in q
        or "work" in q
        or "job" in q
        or "intern" in q
    ):
        # Use the best matching search results
        best_results = results[:3]

        info = []
        for result in best_results:
            text = result.get("text", "").strip()

            if text and text not in info:
                info.append(text)

        if info:
            return " ".join(info)

    # General fallback:
    # use only the strongest result instead of dumping everything
    best_result = results[0]

    return best_result.get(
        "text",
        "I don't have enough information to answer that yet."
    )


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({
            "error": "Please provide a question."
        }), 400

    question = data["question"].strip()

    if not question:
        return jsonify({
            "error": "Please provide a question."
        }), 400

    print(f"Question received: {question}")

    # Search Aishani's knowledge base
    results = search_knowledge(question)

    # Turn search results into a cleaner answer
    answer = generate_answer(question, results)

    return jsonify({
        "question": question,
        "answer": answer,
        "sources": results
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)