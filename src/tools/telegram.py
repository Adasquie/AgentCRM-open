# tools/telegram.py
import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

def send_message(chat_id: str, text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"  # Pour avoir les **gras** dans le message
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"❌ Erreur Telegram : {response.status_code} - {response.text}")
    else:
        print("✅ Message quotidien envoyé avec succès.")