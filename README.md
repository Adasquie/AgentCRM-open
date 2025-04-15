Voici une version complète et soignée de ton README, prête à impressionner aussi bien des utilisateurs que des recruteurs ou des prospects 👇

⸻

🤖 BotLead — Assistant IA de prospection commerciale (Telegram + Airtable + Google)

BotLead, c’est un agent IA connecté à tes outils métiers, qui t’aide à gérer tes leads directement depuis Telegram.
Il automatise les relances, planifie des rendez-vous et garde la mémoire des échanges.
Pensé pour les pros, il est rapide, simple à lancer, et 100% personnalisable.

⸻

⚙️ Fonctionnalités
	•	🔍 Ajout & édition de leads (nom, statut, note…)
	•	🔁 Relance automatique avec planification intelligente
	•	📅 Création de rendez-vous Google Meet via Google Calendar
	•	🧠 Mémoire conversationnelle (10 derniers messages)
	•	📩 Interaction fluide depuis Telegram

⸻

🚀 Lancement local

1. Cloner le projet

git clone https://github.com/ton-user/BotLead.git
cd BotLead

2. Créer un environnement virtuel

python3 -m venv venv
source venv/bin/activate

3. Installer les dépendances

pip install -r requirements.txt

4. Ajouter les variables d’environnement

Crée un fichier .env à la racine :

OPENAI_API_KEY=sk-...
AIRTABLE_API_KEY=...
AIRTABLE_BASE_ID=...
AIRTABLE_TABLE_NAME=...
TELEGRAM_BOT_TOKEN=...
ADMIN_CHAT_ID=...

5. Authentification Google (Calendar + Gmail)

Ajoute manuellement les fichiers suivants dans le dossier auth/ :
	•	credentials.json → depuis Google Cloud Console
	•	token.json → généré automatiquement au premier lancement

📌 Si token.json est absent, une page Google s’ouvrira pour te connecter et générer l’accès (stocké ensuite localement).

⸻

✅ Lancer le bot

python main.py

Tu peux ensuite parler au bot directement via Telegram.
Il répondra automatiquement à tous tes messages.

⸻

🧠 Comment ça marche ?

L’agent IA est orchestré avec le Model Context Protocol (MCP) via le SDK OpenAI Agents.

🔍 Structure du projet :

BotLead/
├── auth/                 # Auth Google (token, credentials)
│   ├── google_auth.py
│   ├── credentials.json
│   └── token.json
├── src/
│   ├── tools/            # Fonctions Airtable, Google, Telegram
│   ├── server/           # MCP tools exposés
│   └── agent_factory.py  # Création de l’agent
├── main.py               # Entrée du bot
├── requirements.txt
├── Procfile              # Pour Railway
├── .env                  # Variables d’environnement (non commit)

🧠 Détails techniques :
	•	Modèle : gpt-4o-2024-11-20
	•	Mémoire : 10 derniers messages par chat_id
	•	MCP tools : calendriers, mails, Airtable, etc.

⸻

☁️ Déploiement Railway
	1.	Connecte ton repo GitHub
	2.	Ajoute les variables d’environnement dans Railway
	3.	Push ton code
	4.	Le Procfile sera détecté automatiquement
	5.	C’est en ligne 🚀

ℹ️ Le container vérifiera automatiquement la présence de credentials.json et token.json au bon endroit (/auth/).
Tu peux les gérer manuellement ou prévoir un mécanisme externe si tu le distribues.

⸻

📜 Licence

BotLead est distribué sous licence GNU AGPL v3 (Affero General Public License).

Cela signifie que :
	•	Tu es libre de l’utiliser, modifier, distribuer et héberger ce projet.
	•	Toute version modifiée déployée publiquement doit également publier son code source.
	•	Tu es responsable de ta propre configuration (API, tokens, sécurité…).

© 2025 Alexandre Dasquié
Pour plus d’infos : gnu.org/licenses/agpl-3.0.html

⸻

👨‍💻 Auteur

Alexandre Dasquié
Créateur d’agents IA sur-mesure pour PME.
Tu veux automatiser les mails, RDV, relances ou extractions ? Parlons-en 👇

📬 LinkedIn : https://www.linkedin.com/in/alexandre-dasquie-796452155/ | ✉️ a.dasquie@gmail.com