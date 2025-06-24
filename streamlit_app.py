import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="🍴 Réservation Restaurant", page_icon="🍽️", layout="centered")

st.markdown("## 🍽️ Assistant de Réservation de Restaurant")
st.markdown("Posez vos questions pour réserver une table, consulter le menu ou connaître les horaires.")

# L'URL de ton backend Flask déployé sur Render
BACKEND_URL = "https://chatbot-api-t3nb.onrender.com/"  # à adapter

# Initialiser la session
if "history" not in st.session_state:
    st.session_state.history = []

# Zone d'entrée utilisateur
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("✍️ Votre message :", placeholder="Je voudrais réserver une table demain à 20h")
    submitted = st.form_submit_button("Envoyer")

# Afficher la conversation
chat_container = st.container()
with chat_container:
    for entry in st.session_state.history:
        role = entry["role"]
        if role == "user":
            st.markdown(f"🧑‍🍳 **Vous** : {entry['content']}")
        else:
            st.markdown(f"🤖 **Bot** : {entry['content']}")

# Envoi du message
if submitted and user_input.strip():
    # Ajout à l'historique
    st.session_state.history.append({"role": "user", "content": user_input})

    with st.spinner("Le bot réfléchit... 🧠"):
        try:
            res = requests.post(BACKEND_URL, json={"message": user_input})
            bot_msg = res.json().get("response", "Je n'ai pas compris, désolé.")
        except Exception as e:
            bot_msg = f"Erreur de connexion au serveur : {e}"

    st.session_state.history.append({"role": "bot", "content": bot_msg})
    st.experimental_rerun()
