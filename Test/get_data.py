import requests
import json
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
DATABASE_ID = os.getenv("DATABASE_ID")

headers =  {
    "Authorization": "Bearer "+ NOTION_API_KEY,
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

def get_pages(num_pages=None):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    
    get_all = num_pages is None
    page_size = 100 if get_all else num_pages
    
    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)
    
    data = response.json()
    
    import json
    with open('db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": ["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])
        
    return results


def get_table():
    pages = get_pages()
    table_data = []
    for page in pages:
        page_id = page["id"]
        props = page.get("properties", {})

        nom = (
            props.get("Nom", {})
            .get("title", [{}])[0]
            .get("text", {})
            .get("content", "Unknown")
        )
        etiquette = (
            props.get("Etiquettes", {})
            .get("rich_text", [{}])[0]
            .get("text", {})
            .get("content", "None")
        )
        date = (
            props.get("Date", {})
            .get("date", {}).
            get("start", None)
        )


        date = datetime.fromisoformat(date)
        
        table_data.append({
            "id": page_id,
            "nom": nom,
            "etiquette": etiquette,
            "date": date.isoformat() if date else None
        })
    return table_data
data = get_table()

for row in data:
    print(row)
    
import json
with open('db_test.json', 'w', encoding='utf8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)



import sqlite3
# Get the absolute path
test_db_path = os.path.abspath("../MrPatachonTest/notion_data.db") 
print(f"Database Path: {test_db_path}")

# Connexion à la base de données SQLite
conn = sqlite3.connect("../notion_data.db")
cursor = conn.cursor()

# Créer une table si elle n'existe pas déjà
cursor.execute('''
CREATE TABLE IF NOT EXISTS notion_data (
    id TEXT PRIMARY KEY,
    nom TEXT,
    etiquette TEXT,
    date TEXT
)
''')

conn.commit()
conn.close()
