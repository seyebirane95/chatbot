from flask import Flask, request, jsonify
from chatbot import NLPChatbot

app = Flask(__name__)
chatbot = NLPChatbot()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    response = chatbot.process_input(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
