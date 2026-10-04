const input = document.getElementById("questionInput");
const chat = document.getElementById("chat");


// Add message to the screen
function addMessage(text, type) {

    const message = document.createElement("div");

    message.classList.add("message");

    if (type === "user") {

        message.classList.add("user-message");

    } else {

        message.classList.add("assistant-message");

        const label = document.createElement("div");

        label.classList.add("message-label");

        label.textContent = "Aishani AI";

        message.appendChild(label);
    }

    const content = document.createElement("span");

    content.textContent = text;

    message.appendChild(content);

    chat.appendChild(message);

    chat.scrollTop = chat.scrollHeight;
}


// Send a question to Flask backend
async function sendMessage() {

    const question = input.value.trim();

    if (question === "") {
        return;
    }

    addMessage(question, "user");

    input.value = "";

    try {

        const response = await fetch("https://aishanis-ai-avatar.onrender.com/ask", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })
        });

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const data = await response.json();

        if (data.answer) {
            addMessage(data.answer, "assistant");
        } else if (data.error) {
            addMessage(data.error, "assistant");
        } else {
            addMessage(
                "I couldn't find an answer to that question.",
                "assistant"
            );
        }

    } catch (error) {

        console.error("Error contacting backend:", error);

        addMessage(
            "I'm having trouble connecting to my backend right now.",
            "assistant"
        );
    }
}


// Suggested question buttons
function askSuggestion(question) {

    input.value = question;

    sendMessage();
}


// Press Enter to send
input.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {

        sendMessage();
    }
});