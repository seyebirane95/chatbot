import spacy
from spacy.matcher import Matcher
import dateparser

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
                return "Certainement ! À quelle date souhaitez-vous réserver ?"
            elif intent == "MENU":
                return "Vous pouvez consulter notre menu sur www.restaurant.com/menu. Autre chose ?"
            elif intent == "HOURS":
                return "Nous sommes ouverts de 11h à 22h tous les jours. Souhaitez-vous réserver ?"
            elif intent == "GREETING":
                return "Bonjour ! Comment puis-je vous aider aujourd’hui ?"
            else:
                return "Je ne suis pas sûr d’avoir compris. Pouvez-vous reformuler ?"

        elif self.state == "ASKING_DATE":
            parsed_date = dateparser.parse(user_input, languages=["fr"])
            if parsed_date:
                date_str = parsed_date.strftime("%d/%m/%Y")
                self.booking_info["date"] = date_str
                self.state = "ASKING_TIME"
                return f"Super ! Vous souhaitez réserver pour le {date_str}. À quelle heure ?"
            else:
                return "Je n’ai pas compris la date. Pouvez-vous la reformuler ?"

        elif self.state == "ASKING_TIME":
            self.booking_info["time"] = user_input
            self.state = "ASKING_PARTY"
            return "Excellent ! Combien de personnes y a-t-il dans votre groupe ?"

        elif self.state == "ASKING_PARTY":
            try:
                party_size = int(user_input)
                self.booking_info["party_size"] = party_size
                self.state = "CONFIRMING"
                return (
                    f"Donc, pour confirmer : {party_size} personnes le {self.booking_info['date']} "
                    f"à {self.booking_info['time']}. C’est bien ça ?"
                )
            except ValueError:
                return "Désolé, je n’ai pas compris le nombre. Combien de personnes êtes-vous ?"

        elif self.state == "CONFIRMING":
            if "oui" in user_input.lower():
                self.state = "GREETING"
                return "Parfait ! Votre réservation est confirmée. À bientôt !"
            else:
                self.state = "GREETING"
                return "D’accord, reprenons depuis le début. Comment puis-je vous aider ?"

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
