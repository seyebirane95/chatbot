import streamlit as st
import spacy
from spacy.matcher import Matcher
import re
from datetime import datetime, timedelta

# Configuration de la page Streamlit
st.set_page_config(
    page_title="🍴 Assistant Restaurant", 
    page_icon="🍽️", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Styles CSS personnalisés
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E8B57;
        font-size: 2.5em;
        margin-bottom: 0.5em;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .user-message {
        background-color: #E3F2FD;
        flex-direction: row-reverse;
    }
    .bot-message {
        background-color: #F1F8E9;
    }
    .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2em;
        margin: 0 10px;
    }
    .user-avatar {
        background-color: #1976D2;
        color: white;
    }
    .bot-avatar {
        background-color: #2E8B57;
        color: white;
    }
    .message-content {
        flex: 1;
        padding: 0 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation du modèle SpaCy (avec gestion d'erreur)
@st.cache_resource
def load_nlp_model():
    try:
        nlp = spacy.load("en_core_web_sm")
        return nlp
    except OSError:
        st.error("⚠️ Le modèle SpaCy 'en_core_web_sm' n'est pas installé. Exécutez: python -m spacy download en_core_web_sm")
        st.stop()

class NLPChatbot:
    def __init__(self):
        self.nlp = load_nlp_model()
        self.matcher = Matcher(self.nlp.vocab)
        self.setup_patterns()
        self.reset_state()
    
    def setup_patterns(self):
        """Configuration des patterns d'intention"""
        self.matcher.add("GREETING", [
            [{"LOWER": {"IN": ["hello", "hi", "hey", "bonjour", "salut"]}}],
            [{"LOWER": "good"}, {"LOWER": {"IN": ["morning", "afternoon", "evening"]}}]
        ])
        
        self.matcher.add("BOOKING", [
            [{"LOWER": {"IN": ["book", "reserve", "reservation", "réserver", "réservation"]}}],
            [{"LOWER": "table"}, {"LOWER": "for"}],
            [{"LOWER": {"IN": ["want", "need"]}}]
        ])
        
        self.matcher.add("MENU", [
            [{"LOWER": {"IN": ["menu", "carte", "food", "eat", "dish"]}}],
            [{"LOWER": "what"}, {"LOWER": {"IN": ["do", "can"]}}]
        ])
        
        self.matcher.add("HOURS", [
            [{"LOWER": {"IN": ["hours", "open", "close", "time", "horaires"]}}],
            [{"LOWER": "when"}, {"LOWER": {"IN": ["open", "close"]}}]
        ])
        
        self.matcher.add("GOODBYE", [
            [{"LOWER": {"IN": ["bye", "goodbye", "exit", "quit", "au revoir"]}}]
        ])
    
    def reset_state(self):
        """Réinitialise l'état du chatbot"""
        self.state = "GREETING"
        self.booking_info = {}
    
    def extract_date_from_text(self, text):
        """Extraction simple de dates"""
        text_lower = text.lower()
        today = datetime.now()
        
        # Mots-clés temporels
        if any(word in text_lower for word in ["today", "aujourd'hui"]):
            return today.strftime("%Y-%m-%d")
        elif any(word in text_lower for word in ["tomorrow", "demain"]):
            return (today + timedelta(days=1)).strftime("%Y-%m-%d")
        elif "next week" in text_lower or "semaine prochaine" in text_lower:
            return (today + timedelta(days=7)).strftime("%Y-%m-%d")
        
        # Recherche de patterns de date
        date_patterns = [
            r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b',  # DD/MM/YYYY ou DD-MM-YYYY
            r'\b(\d{1,2})\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\b',
            r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{1,2})\b'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text_lower)
            if match:
                return match.group(0)
        
        return None
    
    def extract_time_from_text(self, text):
        """Extraction d'heures du texte"""
        time_patterns = [
            r'\b(\d{1,2}):(\d{2})\b',  # HH:MM
            r'\b(\d{1,2})h(\d{2})?\b',  # Xh ou XhMM
            r'\b(\d{1,2})\s*(?:pm|am)\b',  # X pm/am
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(0)
        
        return None
    
    def extract_party_size(self, text):
        """Extraction du nombre de personnes"""
        numbers = re.findall(r'\b(\d+)\b', text)
        if numbers:
            num = int(numbers[0])
            if 1 <= num <= 20:  # Limite raisonnable
                return num
        
        # Mots pour les nombres
        word_to_num = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "un": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
        }
        
        for word, num in word_to_num.items():
            if word in text.lower():
                return num
                
        return None
    
    def get_intent(self, matches):
        """Détermine l'intention principale"""
        if not matches:
            return "UNKNOWN"
        match_id = matches[0][0]
        return self.nlp.vocab.strings[match_id]
    
    def process_input(self, user_input):
        """Traite l'entrée utilisateur selon l'état actuel"""
        doc = self.nlp(user_input)
        matches = self.matcher(doc)
        intent = self.get_intent(matches)
        
        if self.state == "GREETING":
            return self.handle_greeting_state(intent, user_input)
        elif self.state == "ASKING_DATE":
            return self.handle_date_state(user_input)
        elif self.state == "ASKING_TIME":
            return self.handle_time_state(user_input)
        elif self.state == "ASKING_PARTY":
            return self.handle_party_state(user_input)
        elif self.state == "CONFIRMING":
            return self.handle_confirmation_state(user_input)
        
        return "Je ne comprends pas. Pouvez-vous reformuler ?"
    
    def handle_greeting_state(self, intent, user_input):
        """Gère l'état d'accueil"""
        if intent == "BOOKING":
            # Vérifier si des infos sont déjà dans le message
            date = self.extract_date_from_text(user_input)
            time = self.extract_time_from_text(user_input)
            party = self.extract_party_size(user_input)
            
            if date:
                self.booking_info["date"] = date
                if time:
                    self.booking_info["time"] = time
                    if party:
                        self.booking_info["party_size"] = party
                        self.state = "CONFIRMING"
                        return f"Parfait ! Récapitulatif : {party} personne(s) le {date} à {time}. Confirmez-vous cette réservation ?"
                    else:
                        self.state = "ASKING_PARTY"
                        return f"Excellent ! Vous voulez réserver le {date} à {time}. Combien de personnes ?"
                else:
                    self.state = "ASKING_TIME"
                    return f"Super ! Vous voulez réserver le {date}. À quelle heure ?"
            else:
                self.state = "ASKING_DATE"
                return "Bien sûr ! Pour quelle date souhaitez-vous réserver ?"
                
        elif intent == "MENU":
            return "🍽️ Notre menu est disponible sur www.restaurant.com/menu. Nous servons une cuisine française moderne avec des spécialités de saison. Puis-je vous aider avec autre chose ?"
            
        elif intent == "HOURS":
            return "🕐 Nous sommes ouverts tous les jours de 11h00 à 22h00. Souhaitez-vous faire une réservation ?"
            
        elif intent == "GREETING":
            return "Bonjour ! 👋 Bienvenue dans notre restaurant. Comment puis-je vous aider aujourd'hui ?"
            
        elif intent == "GOODBYE":
            return "Au revoir ! 👋 Merci de votre visite. À bientôt !"
            
        else:
            return "Je ne suis pas sûr de comprendre. Vous pouvez me demander de réserver une table, consulter le menu ou connaître nos horaires. Comment puis-je vous aider ?"
    
    def handle_date_state(self, user_input):
        """Gère la demande de date"""
        date = self.extract_date_from_text(user_input)
        if date:
            self.booking_info["date"] = date
            self.state = "ASKING_TIME"
            return f"Parfait ! Vous voulez réserver pour le {date}. À quelle heure ?"
        else:
            return "Je n'ai pas compris la date. Pouvez-vous me dire quand vous souhaitez venir ? (par exemple : demain, 15/06, vendredi...)"
    
    def handle_time_state(self, user_input):
        """Gère la demande d'heure"""
        time = self.extract_time_from_text(user_input)
        if time:
            self.booking_info["time"] = time
            self.state = "ASKING_PARTY"
            return f"Excellent ! Réservation pour le {self.booking_info['date']} à {time}. Combien de personnes ?"
        else:
            return "Je n'ai pas compris l'heure. À quelle heure souhaitez-vous venir ? (par exemple : 19h30, 20:00...)"
    
    def handle_party_state(self, user_input):
        """Gère la demande de nombre de personnes"""
        party_size = self.extract_party_size(user_input)
        if party_size:
            self.booking_info["party_size"] = party_size
            self.state = "CONFIRMING"
            return f"Parfait ! Récapitulatif de votre réservation :\n📅 Date : {self.booking_info['date']}\n🕐 Heure : {self.booking_info['time']}\n👥 Personnes : {party_size}\n\nConfirmez-vous cette réservation ?"
        else:
            return "Je n'ai pas compris le nombre de personnes. Combien serez-vous ? (1, 2, 3...)"
    
    def handle_confirmation_state(self, user_input):
        """Gère la confirmation"""
        response_lower = user_input.lower()
        if any(word in response_lower for word in ["oui", "yes", "ok", "confirme", "confirm", "parfait"]):
            self.state = "GREETING"
            booking_summary = f"""
✅ **Réservation confirmée !**

📅 **Date :** {self.booking_info['date']}
🕐 **Heure :** {self.booking_info['time']}
👥 **Personnes :** {self.booking_info['party_size']}

Nous avons hâte de vous accueillir ! Un email de confirmation vous sera envoyé sous peu.

Y a-t-il autre chose pour laquelle je peux vous aider ?
            """
            self.booking_info = {}  # Reset
            return booking_summary
        else:
            self.state = "GREETING"
            self.booking_info = {}  # Reset
            return "Pas de problème ! Votre réservation a été annulée. Comment puis-je vous aider autrement ?"

# Initialisation du chatbot dans la session Streamlit
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = NLPChatbot()

if 'history' not in st.session_state:
    st.session_state.history = []
    # Message d'accueil initial
    st.session_state.history.append({
        "role": "bot", 
        "content": "Bonjour ! 👋 Bienvenue dans notre restaurant. Comment puis-je vous aider aujourd'hui ?"
    })

# En-tête
st.markdown('<h1 class="main-header">🍽️ Assistant Restaurant</h1>', unsafe_allow_html=True)
st.markdown("---")

# Zone de chat
chat_container = st.container()

# Affichage de l'historique
with chat_container:
    for entry in st.session_state.history:
        if entry["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-content">
                    <strong>Vous :</strong> {entry['content']}
                </div>
                <div class="message-avatar user-avatar">👤</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <div class="message-avatar bot-avatar">🤖</div>
                <div class="message-content">
                    <strong>Assistant :</strong> {entry['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# Zone de saisie
st.markdown("---")
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input(
        "💬 Votre message :", 
        placeholder="Je voudrais réserver une table pour 4 personnes demain à 20h",
        key="user_input"
    )

with col2:
    send_button = st.button("Envoyer 📤", type="primary")
    reset_button = st.button("Reset 🔄")

# Traitement des actions
if send_button and user_input.strip():
    # Ajouter le message utilisateur
    st.session_state.history.append({"role": "user", "content": user_input})
    
    # Traiter avec le chatbot
    with st.spinner("🤔 L'assistant réfléchit..."):
        bot_response = st.session_state.chatbot.process_input(user_input)
    
    # Ajouter la réponse du bot
    st.session_state.history.append({"role": "bot", "content": bot_response})
    
    # Rerun pour actualiser l'affichage
    st.rerun()

if reset_button:
    st.session_state.history = []
    st.session_state.chatbot.reset_state()
    st.session_state.history.append({
        "role": "bot", 
        "content": "Conversation réinitialisée ! Comment puis-je vous aider ?"
    })
    st.rerun()

# Sidebar avec informations
with st.sidebar:
    st.markdown("### ℹ️ Informations")
    st.markdown("""
    **Ce que je peux faire :**
    - 📅 Réserver une table
    - 🍽️ Informations sur le menu
    - 🕐 Horaires d'ouverture
    - 💬 Répondre à vos questions
    
    **Exemples de messages :**
    - "Je voudrais réserver pour 4 personnes"
    - "Quels sont vos horaires ?"
    - "Montrez-moi le menu"
    - "Table pour 2 demain à 19h30"
    """)
    
    st.markdown("---")
    st.markdown("### 🏪 Informations Restaurant")
    st.markdown("""
    **📍 Adresse :** 123 Rue Gourmet, Lyon
    **📞 Téléphone :** 04 xx xx xx xx
    **🕐 Horaires :** 11h00 - 22h00
    **🌐 Site :** www.restaurant.com
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.8em;'>"
    "Powered by Streamlit & SpaCy | Assistant Restaurant v1.0"
    "</div>", 
    unsafe_allow_html=True
)