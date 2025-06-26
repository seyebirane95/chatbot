from flask import Flask, request, jsonify
from chatbot import NLPChatbot  # Assure-toi que ce fichier s'appelle bien chatbot.py

app = Flask(__name__)
bot = NLPChatbot()

@app.route("/", methods=["GET"])
def home():
    return "Chatbot Restaurant API is running."

@app.route("/", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"response": "Erreur : aucun message reçu."}), 400

        user_input = data["message"]
        response = bot.process_input(user_input)
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"response": f"Erreur serveur : {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
