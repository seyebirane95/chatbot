import re
from typing import Dict, List

class Chatbot:
    def __init__(self):
        self.intents: Dict[str, List[str]] = {
            "greeting": ["hello", "hi", "hey"],
            "farewell": ["bye", "goodbye"],
            "thanks": ["thank you", "thanks"],
            "weather": ["weather", "forecast"]
        }
        self.responses: Dict[str, List[str]] = {
            "greeting": ["Hello!", "Hi there!", "Greetings!"],
            "farewell": ["Goodbye!", "See you later!", "Bye!"],
            "thanks": ["You're welcome!", "No problem!", "Glad to help!"],
            "weather": ["I'm sorry, I don't have access to weather information."],
            "unknown": ["I'm not sure how to respond to that.", "Could you please rephrase that?"]
        }

    def messenger(self, user_input: str) -> str:
        intent = self.classifier(user_input)
        entities = self.analyzer(user_input)
        response = self.responder(intent, entities)
        return self.selector(response)

    def classifier(self, user_input: str) -> str:
        user_input = user_input.lower()
        for intent, patterns in self.intents.items():
            for pattern in patterns:
                if re.search(r'\b' + re.escape(pattern) + r'\b', user_input):
                    return intent
        return "unknown"

    def analyzer(self, user_input: str) -> List[str]:
        # Simple entity extraction (just words for now)
        return user_input.lower().split()

    def responder(self, intent: str, entities: List[str]) -> List[str]:
        return self.responses.get(intent, self.responses["unknown"])

    def selector(self, response: List[str]) -> str:
        # For now, just return the first response
        return response[0]

# Utilisation du chatbot
bot = Chatbot()
print("Bot: Hello! I am a simple chatbot. Type 'quit' to exit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        print("Bot: Goodbye!")
        break
    response = bot.messenger(user_input)
    print("Bot:", response)
