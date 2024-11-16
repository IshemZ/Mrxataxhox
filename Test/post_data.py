import requests
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
DATABASE_ID = os.getenv("DATABASE_ID")

headers =  {
    "Authorization": "Bearer "+ NOTION_API_KEY,
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"
    
    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}
    
    res = requests.post(create_url, headers=headers, json=payload)
    print(res.status_code)
    return res

nom = "Wow"
etiquettes = "Non"
date = datetime.now().astimezone(timezone.utc).isoformat()
data = {
    "Nom": {"title": [{"text": {"content": nom}}]},
    "Etiquettes": {"rich_text": [{"text": {"content": etiquettes}}]},
    "Date": {"date": {"text": date, "end": None}}
}

create_page(data)