import os
import requests
from pyairtable import Table
from datetime import date

def get_airtable_table():
    api_key = os.getenv("AIRTABLE_API_KEY")
    base_id = os.getenv("AIRTABLE_BASE_ID")
    table_name = os.getenv("AIRTABLE_TABLE_NAME")

    if not all([api_key, base_id, table_name]):
        raise RuntimeError("❌ Variables d'environnement Airtable manquantes")

    return Table(api_key, base_id, table_name)

def get_airtable_fields() -> list:
    table = get_airtable_table()
    records = table.all(max_records=10)
    all_fields = set()
    for record in records:
        all_fields.update(record.get("fields", {}).keys())
    return sorted(list(all_fields))

def add_prospect(name: str, email: str = None, phone: str = None, company: str = None, source: str = None, statut: str = "New") -> str:
    table = get_airtable_table()
    base_id = os.getenv("AIRTABLE_BASE_ID")
    table_name = os.getenv("AIRTABLE_TABLE_NAME")
    api_key = os.getenv("AIRTABLE_API_KEY")

    url = f"https://api.airtable.com/v0/{base_id}/{table_name}"

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
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return f"✅ Prospect ajouté : {name} ({statut})"
    else:
        return f"❌ Erreur Airtable : {response.status_code} - {response.text}"

def list_prospects(limit=10, filters: dict = None):
    table = get_airtable_table()
    formula = ""
    if filters:
        conditions = [f"{{{field}}} = '{value}'" for field, value in filters.items()]
        formula = "AND(" + ", ".join(conditions) + ")" if len(conditions) > 1 else conditions[0]
        records = table.all(formula=formula, max_records=limit)
    else:
        records = table.all(max_records=limit)
    return records

def update_prospect(record_id: str, fields_to_update: dict) -> str:
    base_id = os.getenv("AIRTABLE_BASE_ID")
    table_name = os.getenv("AIRTABLE_TABLE_NAME")
    api_key = os.getenv("AIRTABLE_API_KEY")

    url = f"https://api.airtable.com/v0/{base_id}/{table_name}/{record_id}"
    data = {"fields": fields_to_update}
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.patch(url, headers=headers, json=data)

    if response.status_code == 200:
        return f"✅ Lead mis à jour ({record_id})"
    else:
        return f"❌ Erreur Airtable : {response.status_code} - {response.text}"

def find_prospect_by_name(name):
    table = get_airtable_table()
    formula = f"FIND(LOWER('{name}'), LOWER({{Lead Name}}))"
    records = table.all(formula=formula)
    return records

def get_leads_to_recontact() -> list:
    table = get_airtable_table()
    today = date.today().isoformat()
    formula = f"IS_SAME({{Date to Recontact}}, '{today}', 'day')"
    return table.all(formula=formula)