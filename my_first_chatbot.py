import re

def simple_chatbot(user_input):
    # Convertir l'entrée en minuscules pour faciliter la correspondance
    user_input = user_input.lower()

    # Définir quelques règles simples
    if re.search(r'\b(hi|hello|hey)\b', user_input):
        return "Hello! How can I help you today?"
    elif re.search(r'\b(bye|goodbye)\b', user_input):
        return "Goodbye! Have a great day!"
    elif re.search(r'\b(thank you|thanks)\b', user_input):
        return "You're welcome!"
    elif re.search(r'\b(weather|forecast)\b', user_input):
        return "I'm sorry, I don't have access to weather information."
    else:
        return "I'm not sure how to respond to that. Can you please rephrase?"

# Boucle principale pour interagir avec le chatbot
print("Chatbot: Hi! I'm a simple rule-based chatbot. Type 'quit' to exit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        print("Chatbot: Goodbye!")
        break
    response = simple_chatbot(user_input)
    print("Chatbot:", response)
