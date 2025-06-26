from flask import Flask, request, jsonify
from chatbot import NLPChatbot

app = Flask(__name__)
bot = NLPChatbot()

@app.route("/")
def home():
    return "Chatbot Restaurant is running."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    response = bot.process_input(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
