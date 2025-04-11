from datetime import datetime
from googleapiclient.discovery import build
from auth.google_auth import get_calendar_service, get_gmail_service
import base64
from email.mime.text import MIMEText

async def create_meet_event(title: str, start_time: str, end_time: str, email: str) -> str:
    service = get_calendar_service()

    event = {
        "summary": title,
        "location": "",
        "description": "Rendez-vous généré par l'agent Telegram.",
        "start": {
            "dateTime": start_time,
            "timeZone": "Europe/Paris",
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "Europe/Paris",
        },
        "attendees": [{"email": email}],
        "guestsCanModify": True,
        "guestsCanSeeOtherGuests": True,
        "conferenceData": {
            "createRequest": {
                "requestId": "tg-agent-meet",  # Un ID unique
                "conferenceSolutionKey": {
                    "type": "hangoutsMeet"
                },
            }
        },
    }

    event = service.events().insert(
        calendarId="primary",
        body=event,
        conferenceDataVersion=1,
        sendUpdates="all"  # ✅ ENVOI des mails
    ).execute()

    meet_link = event["hangoutLink"]
    return f"✅ Rendez-vous créé !\nVoici le lien Google Meet : [{meet_link}]({meet_link})"

def list_events_for_day(date_str: str = None) -> list:
    """Liste les événements pour une date donnée (au format YYYY-MM-DD), ou pour aujourd’hui si vide."""
    service = get_calendar_service()

    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        date = datetime.now()

    start_time = date.replace(hour=0, minute=0, second=0).isoformat()
    end_time = date.replace(hour=23, minute=59, second=59).isoformat()

    events_result = service.events().list(
        calendarId="primary",
        timeMin=start_time + "+01:00",
        timeMax=end_time + "+01:00",
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])
    return [
        {
            "summary": event.get("summary", "📌 Sans titre"),
            "start": str(event["start"].get("dateTime", event["start"].get("date"))),
            "end": str(event["end"].get("dateTime", event["end"].get("date"))),
        }
        for event in events
    ]

def create_email_draft(recipient: str, subject: str, body: str, sender: str = "me") -> str:
    service = get_gmail_service()

    message = MIMEText(body)
    message["to"] = recipient
    message["from"] = sender
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    draft = service.users().drafts().create(
        userId=sender,
        body={"message": {"raw": raw}}
    ).execute()

    return f"✅ Brouillon créé pour {recipient} avec le sujet : {subject}"