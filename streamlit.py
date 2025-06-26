import streamlit as st
import requests

# Config Streamlit
st.set_page_config(page_title="Assistant Restaurant", page_icon="🍽️")
st.title("🍽️ Assistant Restaurant")

API_URL = "https://chatbot-api-t3nb.onrender.com/"  # Remplace par l'URL réelle de ton backend Render

if 'history' not in st.session_state:
    st.session_state.history = [{"role": "bot", "content": "Bonjour ! Comment puis-je vous aider ?"}]

# Affichage des messages
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(f"**Vous :** {msg['content']}")
    else:
        st.markdown(f"**Assistant :** {msg['content']}")

user_input = st.text_input("💬 Votre message :", key="input")
if st.button("Envoyer") and user_input.strip():
    st.session_state.history.append({"role": "user", "content": user_input})
    try:
        res = requests.post(API_URL, json={"message": user_input})
        bot_msg = res.json().get("response", "Erreur serveur.")
    except Exception as e:
        bot_msg = f"Erreur : {e}"
    st.session_state.history.append({"role": "bot", "content": bot_msg})
    st.rerun()
