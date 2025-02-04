from fastapi import FastAPI
from pymongo import MongoClient
import uvicorn
import threading
import gradio as gr
import requests
from fastapi.responses import HTMLResponse

app = FastAPI()

# Connexion à MongoDB
my_db = "mongodb://localhost:27017/"
client = MongoClient(my_db)
db = client["dataset"]  # Nom de la base de données
collection = db["Photo"]  # Collection dans la base de données
from fastapi.middleware.cors import CORSMiddleware

# Ajoutez ce middleware après avoir initialisé `app`
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Origine de votre app React
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes HTTP
    allow_headers=["*"],  # Autoriser tous les headers
)


@app.get("/", response_model=list[dict])
def get_photos():
    """
    Récupérer les 20 premiers documents avec les champs Label et Repartition.
    """
    # Projection pour récupérer seulement les champs 'Label' et 'Repartition'
    projection = {"Label": 1, "Repartition": 1, "_id": 0}  # Exclure '_id'
    
    # Récupérer les 20 premiers documents
    photos = list(collection.find({}, projection).limit(20))  # Limiter à 20 documents
    
    return photos

# Lancer FastAPI
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Lancer FastAPI dans un thread
if __name__ == "__main__":
    fastapi_thread = threading.Thread(target=run_fastapi)
    fastapi_thread.start()
