import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 📂 Emplacement des fichiers d’auth
BASE_DIR = os.path.dirname(__file__)
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")
CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")

# 🔐 Scopes nécessaires (accès à Google Calendar avec génération de lien Meet)
SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/gmail.compose",  # 👈 pour créer un brouillon
    "https://www.googleapis.com/auth/gmail.modify",   # 👈 optionnel si tu veux manipuler les mails ensuite
    "https://www.googleapis.com/auth/gmail.send"      # 👈 utile pour envoyer automatiquement plus tard
]

def get_calendar_service():
    """
    Récupère un service Google Calendar authentifié avec génération automatique de token.
    Si aucun token ou token expiré, lance un flow OAuth sur http://localhost:8080
    """
    creds = None

    # Charge le token s’il existe
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # Rafraîchit ou crée un nouveau token si nécessaire
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=8080)

        # Sauvegarde le nouveau token
        with open(TOKEN_PATH, 'w') as token_file:
            token_file.write(creds.to_json())

    # Retourne un client Google Calendar prêt à l'emploi
    return build("calendar", "v3", credentials=creds)

def get_gmail_service():
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("👉 Lancement du flow d'auth Gmail...")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=8080)

        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

if __name__ == "__main__":
    service = get_gmail_service()
    print("✅ Connexion à Gmail réussie !")