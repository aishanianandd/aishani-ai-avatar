from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.knowledge import search_knowledge
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "Aishani AI backend is running!"
    })


def generate_answer(question, results):
    if not results:
        return (
            "I don't have enough information about Aishani "
            "to answer that question yet."
        )

    context = "\n".join(
        result.get("text", "")
        for result in results[:5]
        if result.get("text")
    )

    response = client.responses.create(
        model="gpt-5-mini",
        instructions=(
            "You are Aishani AI, an AI portfolio assistant for Aishani Anand. "
            "Answer questions about Aishani using only the provided context. "
            "Speak naturally and professionally, as if you are representing "
            "Aishani's portfolio. Do not invent experience, skills, projects, "
            "or facts that are not in the context. If the context does not "
            "contain enough information, say that you don't have enough "
            "information to answer."
        ),
        input=f"""
Question:
{question}

Context about Aishani:
{context}
"""
    )

    return response.output_text


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
    app.run(debug=True, port=5001)