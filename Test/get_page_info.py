import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Informations nécessaires
api_key = os.getenv('api_key')
page_id = os.getenv('page_id')

# URL pour l'API Notion
url = f"https://api.notion.com/v1/pages/{page_id}"

# Headers requis
headers = {
    "Authorization": f"Bearer {api_key}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

# Requête GET
response = requests.get(url, headers=headers)

# Vérification de la réponse
if response.status_code == 200:
    data = response.json()
    print("Données de la page Notion récupérées :")
    print(data)
else:
    print("Erreur lors de la requête :", response.status_code)
    print(response.text)
