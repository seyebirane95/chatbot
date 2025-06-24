
# 🍽️ Assistant Chatbot Restaurant

Un assistant conversationnel intelligent pour gérer les réservations, répondre aux questions sur le menu et les horaires d’un restaurant.

---

## 📋 Description

Ce projet propose un chatbot capable de comprendre les demandes des clients, notamment pour réserver une table, connaître les horaires d’ouverture ou consulter le menu. L’interface graphique est réalisée avec **Streamlit**, tandis que la logique NLP et la gestion des conversations sont encapsulées dans une API Flask déployée sur **Render**.

---

## 🚀 Fonctionnalités

* Dialogue interactif avec gestion d’état conversationnel
* Reconnaissance d’intentions via SpaCy (réservation, menu, horaires, salutations)
* Extraction de données : date, heure, nombre de personnes
* Interface utilisateur simple et ergonomique avec historique de chat
* Architecture client-serveur avec API REST

---

## 📁 Structure du projet

```
chatbot_restaurant/
│
├── chatbot.py         # Moteur NLP (classe NLPChatbot)
├── app.py             # Backend API Flask (Render)
├── streamlit_app.py   # Interface graphique Streamlit
├── requirements.txt   # Dépendances Python
├── Procfile           # Commande de lancement pour Render
└── README.md          # Ce fichier
```

---

## ⚙️ Installation et déploiement local

1. Cloner le projet :

   ```bash
   git clone https://github.com/ton-utilisateur/chatbot_restaurant.git
   cd chatbot_restaurant
   ```

2. Créer un environnement virtuel et installer les dépendances :

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. Lancer l’API Flask :

   ```bash
   python app.py
   ```

   L’API sera disponible sur [http://127.0.0.1:5000/chat](http://127.0.0.1:5000/chat)

4. Lancer l’interface Streamlit dans un autre terminal :

   ```bash
   streamlit run streamlit_app.py
   ```

---

## 🌐 Déploiement en production

* **Backend** : déployer `app.py` sur Render ([https://render.com](https://render.com))
* **Frontend** : déployer `streamlit_app.py` sur Streamlit Cloud ([https://share.streamlit.io](https://share.streamlit.io))

---

## 🔧 Utilisation

* Dans l’interface Streamlit, entrez votre message dans le champ de saisie.
* Le message est envoyé à l’API qui traite la requête et renvoie une réponse intelligente.
* L’historique de la conversation est affiché pour un suivi fluide.

---

## 📚 Technologies utilisées

* Python 3.9+
* Flask (API REST)
* SpaCy (NLP)
* Streamlit (interface utilisateur)
* Render (hébergement backend)
* Streamlit Cloud (hébergement frontend)

---

## 🤝 Contribution

N’hésitez pas à proposer des améliorations via des issues ou des pull requests.

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus d’informations.
