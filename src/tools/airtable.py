import os
import requests
from dotenv import load_dotenv
from pyairtable import Table
from datetime import datetime, date

load_dotenv()

API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")

table = Table(API_KEY, BASE_ID, TABLE_NAME)

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_airtable_fields() -> list:
    """
    Retourne tous les noms de colonnes uniques présents dans Airtable.
    Parcourt les 10 premiers enregistrements si besoin.
    """
    records = table.all(max_records=10)
    all_fields = set()
    for record in records:
        all_fields.update(record.get("fields", {}).keys())
    return sorted(list(all_fields))

def add_prospect(
    name: str,
    email: str = None,
    phone: str = None,
    company: str = None,
    source: str = None,
    statut: str = "New"
) -> str:
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"


    fields = {
        "Lead Name": name,
        "Status": statut,
    }

    if email:
        fields["Contact Information"] = email
    if phone:
        fields["Phone"] = phone
    if company:
        fields["Company"] = company
    if source:
        fields["Lead Source"] = source

    data = {"fields": fields}
    response = requests.post(url, headers=HEADERS, json=data)

    if response.status_code == 200:
        return f"✅ Prospect ajouté : {name} ({statut})"
    else:
        return f"❌ Erreur Airtable : {response.status_code} - {response.text}"
    
def list_prospects(limit=10, filters: dict = None):
    """
    Liste les prospects avec un filtre dynamique.
    Tu peux filtrer par n’importe quel champ (ex: Status, Company, Source…).
    
    Exemple :
    list_prospects(limit=5, filters={"Status": "R1", "Company": "m2web"})
    """
    formula = ""
    if filters:
        conditions = [f"{{{field}}} = '{value}'" for field, value in filters.items()]
        formula = "AND(" + ", ".join(conditions) + ")" if len(conditions) > 1 else conditions[0]
        records = table.all(formula=formula, max_records=limit)
    else:
        records = table.all(max_records=limit)

    return records

def update_prospect(record_id: str, fields_to_update: dict) -> str:

    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}/{record_id}"
    data = {"fields": fields_to_update}

    response = requests.patch(url, headers=HEADERS, json=data)

    if response.status_code == 200:
        return f"✅ Lead mis à jour ({record_id})"
    else:
        return f"❌ Erreur Airtable : {response.status_code} - {response.text}"
    
def find_prospect_by_name(name):
    formula = f"FIND(LOWER('{name}'), LOWER({{Lead Name}}))"
    records = table.all(formula=formula)
    return records

def get_leads_to_recontact() -> list:
    """
    Récupère les leads dont la 'Date to Recontact' est aujourd’hui.
    """
    today = date.today().isoformat()
    formula = f"IS_SAME({{Date to Recontact}}, '{today}', 'day')"
    return table.all(formula=formula)