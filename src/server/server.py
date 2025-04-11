from mcp.server.fastmcp import FastMCP
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.tools import airtable, google, telegram


mcp = FastMCP("Prospection MCP Server")

@mcp.tool()
def get_available_fields() -> str:
    champs = airtable.get_airtable_fields()
    if not champs:
        return "❌ Aucun champ détecté dans Airtable."
    return "📋 Champs disponibles dans Airtable :\n\n" + "\n".join([f"- {c}" for c in champs])

@mcp.tool()
def add_prospect(
    name: str,
    email: str = None,
    phone: str = None,
    company: str = None,
    source: str = None,
    statut: str = "New"
) -> str:
    return airtable.add_prospect(name, email, phone, company, source, statut)

@mcp.tool()
def list_prospects(limit: int = 10, filters: dict = None) -> str:
    """
    📋 Liste les prospects depuis Airtable.

    Tu peux afficher les X derniers prospects (avec `limit`) ou filtrer par statut :
    - New
    - Contacted
    - R1
    - R2
    - Propal
    - Closed
    - Not interested

    Exemples :
    - `list_prospects(limit=5)`
    - `list_prospects(statut_filter="New")`
    - `list_prospects(limit=3, statut_filter="R1")`
    """
    return airtable.list_prospects(limit, filters)

@mcp.tool()
def update_prospect(record_id: str, fields_to_update: dict) -> str:
    """
    🔧 Met à jour un prospect existant dans Airtable.

    ✳️ Tu dois fournir :
    - record_id : ID unique du prospect (ex: "recXXXXXXX")
    - fields_to_update : un dictionnaire avec les modifications à faire, ex:
        {"Status": "New"} ou {"Lead Name": "Julie Dupont"}

    ⚠️ Le nom des champs doit correspondre exactement à ceux d’Airtable.
    Si on te dit rajoute une info, tu dois la rajouter en plus de l'info déjà existante notamment dans notes en ajoutant la date.
    exemple : 
    "2025-04-10 14:00 : Le client souhaite être contacté par mail"
    """
    if not fields_to_update:
        return "❌ Erreur : aucun champ fourni à mettre à jour. Fournis un dictionnaire comme {'Status': 'New'}."

    try:
        response = airtable.update_prospect(record_id, fields_to_update)
        return f"✅ Prospect mis à jour avec succès : {fields_to_update}"
    except Exception as e:
        return f"❌ Erreur lors de la mise à jour : {str(e)}"

@mcp.tool()
def find_prospect_by_name(name: str) -> str:
    return airtable.find_prospect_by_name(name)


@mcp.tool()
async def create_meet_event(title: str, start_time: str, end_time: str, email: str) -> str:
    """
    📅 Crée un événement Google Meet.

    🔹 Titre : Formate-le comme ceci → "Echange - Alexandre x Prénom"
    🔹 start_time / end_time : format RFC3339 (ex: 2025-04-03T14:00:00+01:00)
    🔹 email : adresse de l'invité

    🧠 Tu dois générer un titre clair à partir du nom du participant.
    """
    return await google.create_meet_event(title, start_time, end_time, email)

@mcp.tool()
def list_events_for_day(date: str = "") -> list:
    """
    Liste les événements pour une date donnée (YYYY-MM-DD), ou aujourd’hui si aucun paramètre.
    """
    return google.list_events_for_day(date or None)

@mcp.tool()
def create_email_draft(recipient: str, subject: str, body: str) -> str:
    """
    📧 Génère un brouillon d’email Gmail à vérifier avant envoi.
    Tu dois fournir le destinataire, le sujet, et le contenu (body).
    Le mail ne sera pas envoyé automatiquement.
    """
    return google.create_email_draft(recipient, subject, body)

@mcp.tool()
def leads_to_follow_up_today() -> str:
    leads = airtable.get_leads_to_recontact()
    if not leads:
        return "📭 Aucun lead à recontacter aujourd’hui."

    messages = []
    for lead in leads:
        fields = lead.get("fields", {})
        name = fields.get("Lead Name", "Inconnu")
        statut = fields.get("Status", "Non défini")
        note = fields.get("Notes", "Pas de note.")
        messages.append(f"- **{name}** ({statut}) → {note.splitlines()[-1]}")

    return "📅 Leads à recontacter aujourd’hui :\n\n" + "\n".join(messages)

@mcp.tool()
def send_daily_reminder() -> str:
    """
    Envoie un message quotidien à l'admin.
    """
    return telegram.send_daily_reminder()

if __name__ == "__main__":
    mcp.run(transport="stdio")