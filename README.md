# 🤖 BotLead — Assistant de prospection IA (Telegram + Airtable)

BotLead est un assistant IA de prospection automatisée connecté à :
- 🧠 OpenAI GPT-4o
- 🗂️ Airtable (gestion de leads)
- 📅 Google Calendar (prise de RDV)
- 💬 Telegram (interface utilisateur)

L’agent t’aide à :
- Ajouter/modifier des prospects
- Planifier des rappels automatiques
- Créer des événements Google Meet
- Suivre et relancer les leads facilement

---

## 🚀 Lancement local

### 1. Clone du projet

```bash
git clone https://github.com/ton-user/BotLead.git
cd BotLead

2. Création d’un environnement virtuel

python3 -m venv venv
source venv/bin/activate

3. Installation des dépendances
pip install -r requirements.txt

4. Variables d’environnement

OPENAI_API_KEY=sk-...
AIRTABLE_API_KEY=...
AIRTABLE_BASE_ID=...
AIRTABLE_TABLE_NAME=...
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...

5. Lancement
python main.py

BotLead/
├── auth/                 # Auth Google (token, credentials)
│   ├── google_auth.py
│   ├── credentials.json
│   └── token.json
├── src/
│   ├── tools/            # Fonctions Airtable, Google, Telegram
│   └── server/           # MCP tools exposés
│   ├── agent_factory.py  # Création de l’agent
├── main.py               # Entrée du bot
├── requirements.txt      # Dépendances
├── Procfile              # Pour Railway
├── .env                  # Variables d’environnement (non commit)

🛠 Stack technique
	•	Python 3.11+
	•	OpenAI Agent SDK (MCP)
	•	Airtable + Google API
	•	Telegram Bot
	•	Railway (déploiement)

🧠 Fonctionnement de l’agent

L’agent est orchestré via MCP (Model Context Protocol) :
	•	Tools : déclarés dans src/server/server.py
	•	Mémoire : 10 derniers messages Telegram
	•	Modèle : gpt-4o-2024-11-20
	•	Interaction : naturelle, rapide, fluide


⸻

📦 Déploiement Railway
	1.	Connecte ton repo GitHub
	2.	Ajoute les variables d’environnement
	3.	Railway détectera automatiquement le Procfile
	4.	C’est parti 🚀

🧑‍💻 Auteur

Créé par Alexandre Dasquié — automatisation IA pour PME.