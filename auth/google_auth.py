import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 📂 Emplacement des fichiers d’auth
BASE_DIR = os.path.dirname(__file__)
TOKEN_PATH = os.getenv("GOOGLE_TOKEN_PATH") or os.path.join(BASE_DIR, "auth", "token.json")
CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH") or os.path.join(BASE_DIR, "auth", "credentials.json")

# 🔐 Scopes nécessairesimport os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 📂 Emplacement des fichiers d’auth
TOKEN_PATH = os.getenv("GOOGLE_TOKEN_PATH") or "/app/auth/token.json"
CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH") or "/app/auth/credentials.json"

# 🔐 Scopes nécessaires
SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send"
]

def get_calendar_service():
    creds = _load_credentials()
    return build("calendar", "v3", credentials=creds)

def get_gmail_service():
    creds = _load_credentials()
    return build("gmail", "v1", credentials=creds)

def _load_credentials():
    creds = None

    print(f"🔍 Looking for credentials at: {CREDENTIALS_PATH}")
    print(f"🔍 Looking for token at: {TOKEN_PATH}")

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=8080)  # Utilisé localement uniquement

        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())

    return creds

if __name__ == "__main__":
    service = get_gmail_service()
    print("✅ Connexion à Gmail réussie !")
SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send"
]

def get_calendar_service():
    creds = _load_credentials()
    return build("calendar", "v3", credentials=creds)

def get_gmail_service():
    creds = _load_credentials()
    return build("gmail", "v1", credentials=creds)

def _load_credentials():
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("🔐 Aucun token valide trouvé. Lancement du flow OAuth...")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=8080)  # Local login flow

        # Sauvegarde du nouveau token
        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())

    return creds

if __name__ == "__main__":
    service = get_gmail_service()
    print("✅ Connexion à Gmail réussie !")