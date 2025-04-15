import os
import tempfile
import asyncio
from datetime import date
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler

from openai import OpenAI
from agents import Runner


print("🚨 DEBUG ENV VARS")
print("AIRTABLE_API_KEY:", os.getenv("AIRTABLE_API_KEY"))
print("BASE_ID:", os.getenv("AIRTABLE_BASE_ID"))
print("TABLE_NAME:", os.getenv("AIRTABLE_TABLE_NAME"))

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
application = Application.builder().token(TELEGRAM_TOKEN).build()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Remplis avec ton chat_id fixe si connu
CHAT_ID = os.getenv("ADMIN_CHAT_ID") or None

print("🚨 DEBUG ENV VARS")
print("AIRTABLE_API_KEY:", os.getenv("AIRTABLE_API_KEY"))
print("BASE_ID:", os.getenv("AIRTABLE_BASE_ID"))
print("TABLE_NAME:", os.getenv("AIRTABLE_TABLE_NAME"))

from src.agent_factory import create_prospect_agent
from src.tools import memory, airtable, telegram

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ID
    CHAT_ID = update.effective_chat.id
    print(f"chat_id = {CHAT_ID}")
    await update.message.reply_text(f"Ton chat_id est : {CHAT_ID}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_input = update.message.text
    chat_id = update.effective_chat.id
    memory.add_interaction(user_input, role="user")
    
    server_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "src", "server", "server_mcp.py"))
    agent = await create_prospect_agent(server_file, chat_id)

    result = await Runner.run(agent, input=user_input)
    await context.bot.send_message(chat_id=chat_id, text=result.final_output or "Je n'ai pas compris.")
    memory.add_interaction(result.final_output, role="assistant")

async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    voice = update.message.voice or update.message.audio
    if not voice:
        return

    file = await context.bot.get_file(voice.file_id)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as f:
        await file.download_to_drive(f.name)
        audio_path = f.name

    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(model="gpt-4o-transcribe", file=audio_file)

    transcribed_text = transcript.text
    memory.add_interaction(transcribed_text, role="user")

    server_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "server_mcp.py"))
    agent = await create_prospect_agent(server_file, chat_id)

    result = await Runner.run(agent, input=transcribed_text)
    await context.bot.send_message(chat_id=chat_id, text=result.final_output or "Je n'ai pas compris.")
    memory.add_interaction(result.final_output, role="assistant")
    os.remove(audio_path)

def send_daily_reminder():
    if not CHAT_ID:
        print("Aucun chat_id défini pour le rappel quotidien.")
        return

    leads = airtable.get_leads_to_recontact()
    if not leads:
        message = "📭 Aucun lead à recontacter aujourd’hui."
    else:
        message = "📅 Leads à recontacter aujourd’hui :\n\n"
        for lead in leads:
            fields = lead.get("fields", {})
            name = fields.get("Lead Name", "Inconnu")
            statut = fields.get("Status", "Non défini")
            note = fields.get("Notes", "Pas de note.")
            message += f"- {name} ({statut}) → {note.splitlines()[-1]}\n"

    telegram.send_message(CHAT_ID, message)

# 🔁 Lancement du scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(send_daily_reminder, 'cron', hour=8, minute=0)
scheduler.start()

if __name__ == "__main__":

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_voice_message))
    print("✅ Bot Lead prêt. Envoie un message sur Telegram pour commencer.")
    application.run_polling()