import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

# Patterns d’intention
matcher.add("GREETING", [[{"LOWER": {"IN": ["hello", "hi", "hey"]}}]])
matcher.add("BOOKING", [[{"LOWER": {"IN": ["book", "reserve", "reservation"]}}]])
matcher.add("MENU", [[{"LOWER": "menu"}]])
matcher.add("HOURS", [[{"LOWER": {"IN": ["hours", "open"]}}]])

class NLPChatbot:
    def __init__(self):
        self.state = "GREETING"
        self.booking_info = {}

    def process_input(self, user_input):
        doc = nlp(user_input)
        matches = matcher(doc)
        intent = self.get_intent(matches)
        entities = self.extract_entities(doc)

        if self.state == "GREETING":
            if intent == "BOOKING":
                self.state = "ASKING_DATE"
                return "Certainly! What date would you like to book?"
            elif intent == "MENU":
                return "You can find our menu at www.restaurant.com/menu. Anything else?"
            elif intent == "HOURS":
                return "We're open from 11 AM to 10 PM every day. Would you like to make a reservation?"
            elif intent == "GREETING":
                return "Hello! How can I assist you today?"
            else:
                return "I'm not sure I understood that. Could you please rephrase?"
        
        elif self.state == "ASKING_DATE":
            if "DATE" in entities:
                self.booking_info["date"] = entities["DATE"]
                self.state = "ASKING_TIME"
                return f"Great! You want to book for {entities['DATE']}. What time?"
            else:
                return "Could you tell me the date again?"

        elif self.state == "ASKING_TIME":
            self.booking_info["time"] = user_input
            self.state = "ASKING_PARTY"
            return "Excellent! How many people are in your party?"

        elif self.state == "ASKING_PARTY":
            try:
                party_size = int(user_input)
                self.booking_info["party_size"] = party_size
                self.state = "CONFIRMING"
                return f"So, to confirm: {party_size} people on {self.booking_info['date']} at {self.booking_info['time']}. Is that correct?"
            except ValueError:
                return "Sorry, I didn't understand the number. How many people are in your party?"

        elif self.state == "CONFIRMING":
            if "yes" in user_input.lower():
                self.state = "GREETING"
                return "Perfect! Your reservation is confirmed. Looking forward to seeing you!"
            else:
                self.state = "GREETING"
                return "Okay, let's start over. How can I assist you?"

    def get_intent(self, matches):
        if not matches:
            return "UNKNOWN"
        match_id = matches[0][0]
        return nlp.vocab.strings[match_id]

    def extract_entities(self, doc):
        entities = {}
        for ent in doc.ents:
            entities[ent.label_] = ent.text
        return entities

# Utilisation
bot = NLPChatbot()
print("Bot: Welcome to our restaurant! How can I assist you today?")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("Bot: Thank you for using our service. Goodbye!")
        break
    response = bot.process_input(user_input)
    print("Bot:", response)
