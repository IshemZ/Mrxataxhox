import requests
import sqlite3
import os
# Variables API Notion
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
DATABASE_ID = os.getenv("DATABASE_ID")   

headers =  {
    "Authorization": "Bearer "+ NOTION_API_KEY,
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}
url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
response = requests.get(url, headers=headers)
if response.status_code == 200:
    print("Database ID is valid!")
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.json())


# En-têtes pour les requêtes API
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# Récupérer les données depuis l'API Notion
url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
response = requests.post(url, headers=headers)
data = response.json()

# Vérifiez si la requête a réussi
if response.status_code == 200:
    print("Données récupérées avec succès.")
else:
    print(f"Erreur: {response.status_code}")
    print(data)

# Extraire et afficher les résultats
for result in data.get("results", []):
    print(result) # Inspectez la structure des données ici



# Get the absolute path
test_db_path = os.path.abspath("../MrPatachon/Database/test.db") 
print(f"Database Path: {test_db_path}")


# Create a connection to the database
conn = sqlite3.connect(test_db_path)

# Create a cursor object
cursor = conn.cursor()

# Create a table
cursor.execute(''' CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER
)
''')

# Insert data
cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ("John Doe", 30))

# Commit changes and close the connection
conn.commit()
conn.close()
