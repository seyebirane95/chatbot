import streamlit as st
import requests
import time

# Config Streamlit
st.set_page_config(page_title="Assistant Restaurant", page_icon="🍽️", layout="centered")
st.markdown("<h1 style='text-align:center;'>🍽️ Assistant Restaurant</h1>", unsafe_allow_html=True)

# Bouton reset dans la sidebar
with st.sidebar:
    if st.button("🔁 Réinitialiser le chat"):
        st.session_state.history = [{"role": "bot", "content": "Bonjour ! Comment puis-je vous aider ?"}]
        st.experimental_rerun()

API_URL = "https://chatbot-api-t3nb.onrender.com/"

# Initialisation de l'historique
if "history" not in st.session_state:
    st.session_state.history = [{"role": "bot", "content": "Bonjour ! Comment puis-je vous aider ?"}]

# Affichage des messages avec style bulles
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(
            f"<div style='text-align:right; background:#DCF8C6; border-radius:10px; padding:8px; margin:5px 0;'>{msg['content']}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='text-align:left; background:#F1F0F0; border-radius:10px; padding:8px; margin:5px 0;'>{msg['content']}</div>",
            unsafe_allow_html=True,
        )

# Input utilisateur dans formulaire avec clear_on_submit=True
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "💬 Entrez votre message :", label_visibility="collapsed", placeholder="Posez votre question..."
        )
        submitted = st.form_submit_button("Envoyer")

# Traitement du message envoyé
if submitted and user_input.strip():
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.spinner("L'assistant réfléchit..."):
        try:
            res = requests.post(API_URL, json={"message": user_input})
            bot_msg = res.json().get("response", "Erreur serveur.")
        except Exception as e:
            bot_msg = f"Erreur : {e}"
        time.sleep(0.3)
        st.session_state.history.append({"role": "bot", "content": bot_msg})
        st.experimental_rerun()
