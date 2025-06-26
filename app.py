
import os
from flask import Flask, request, jsonify
from chatbot import NLPChatbot

app = Flask(__name__)
chatbot = NLPChatbot()

@app.route("/", methods=["GET"])
def home():
    return "Chatbot API is running!"

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    return jsonify({"response": f"Vous avez dit : {user_input}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
