# from fastapi import FastAPI
# from pymongo import MongoClient
# import uvicorn
# import threading
# import gradio as gr
# import requests
# from fastapi.responses import HTMLResponse

# app = FastAPI()

# # Connexion à MongoDB
# my_db = "mongodb://localhost:27017/"
# client = MongoClient(my_db)
# db = client["dataset"]  # Nom de la base de données
# collection = db["Photo"]  # Collection dans la base de données
# from fastapi.middleware.cors import CORSMiddleware

# # Ajoutez ce middleware après avoir initialisé `app`
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Origine de votre app React
#     allow_credentials=True,
#     allow_methods=["*"],  # Autoriser toutes les méthodes HTTP
#     allow_headers=["*"],  # Autoriser tous les headers
# )


# @app.get("/", response_model=list[dict])
# def get_photos():
#     """
#     Récupérer les 20 premiers documents avec les champs Label et Repartition.
#     """
#     # Projection pour récupérer seulement les champs 'Label' et 'Repartition'
#     projection = {"Label": 1, "Repartition": 1, "_id": 0}  # Exclure '_id'
    
#     # Récupérer les 20 premiers documents
#     photos = list(collection.find({}, projection).limit(20))  # Limiter à 20 documents
    
#     return photos

# # Lancer FastAPI
# def run_fastapi():
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# # Lancer FastAPI dans un thread
# if __name__ == "__main__":
#     fastapi_thread = threading.Thread(target=run_fastapi)
#     fastapi_thread.start()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import random
from PIL import Image
import tensorflow as tf
import os
import json
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Exemple de données aléatoires
CHEMAIN = ["../../Dataset"]  # Remplace par ta liste de fichiers d'images

# Ajouter le middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet les requêtes de n'importe quelle origine (ou adapte selon tes besoins)
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes HTTP
    allow_headers=["*"],  # Permet tous les en-têtes
)

# Le reste de ton code FastAPI suit ici...

# Initialisation des variables
TYPE = {0: 'MAJ', 1: 'MIN', 2: 'NBR'}
MAJ = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'}
MIN = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z'}
NBR = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9'}
CHEMAIN = []

# Chargement des modèles
model_type = tf.keras.models.load_model("../../Yann\models\Get_Nbr_v4_b32_e10.keras")
model_maj = tf.keras.models.load_model("../../Yann\models\Get_Nbr_v4_b32_e10.keras")
model_min = tf.keras.models.load_model("../../Yann\models\Get_Nbr_v4_b32_e10.keras")
model_nbr = tf.keras.models.load_model("../../Yann\models\Get_Nbr_v4_b32_e10.keras")

def format_image(chemin: str) -> np.ndarray:
    """_summary_

    Args:
        chemin (str): _description_

    Returns:
        np.ndarray: _description_
    """
    img = Image.open(chemin) # 300 x 300
    
    nouvelle_taille = (25, 25) # 625
    
    img_redimensionnee = img.resize(nouvelle_taille) # Redimensionner l'image
    nb_image = img_redimensionnee.convert('L') # Convertion en noir et blanc
    
    tab = []
    for i in range(nb_image.size[1]):
        row = []
        for y in range(nb_image.size[0]):
            # Récupérer la couleur du pixel
            row.append(nb_image.getpixel((y, i)))
        tab.append(row)
        
    tab_numpy = np.array(tab) / 255 # mise à l'échelle des données
    tab_numpy_flatten = tab_numpy.flatten() # Transformation en tableau 1D
    
    return tab_numpy_flatten # Retourner le tableau de pixels

# Parcours des dossiers et sous-dossiers pour récupérer les chemins de toutes les photos (recursion)
def recup_chemin(chemin: str) -> None:
    """Summary ______________________________________________________________

    Args:
        chemin (str): chemin du dataset
    """
    dossiers = [f for f in os.listdir(chemin) if os.path.isdir(os.path.join(chemin, f))]
    if len(dossiers) == 0: # Si aucun dossier n'est trouvé, on est dans le cas de base
        fichiers_png = [os.path.join(chemin, f) for f in os.listdir(chemin) if f.endswith('.png')] # on recupère et stocke les fichiers .png
        CHEMAIN.extend(fichiers_png) # on ajoute les chemins des fichiers .png dans une liste
    else : # Sinon, on continue de parcourir les dossiers
        for dossier in dossiers:
            recup_chemin(os.path.join(chemin, dossier))

def predict_image(chemin: str) -> json:
    """_summary_

    Args:
        chemin (str): chemin de l'image à prédire

    Returns:
        JSON: json contenant, le chemin de l'image, la prédiction finale et les prédictions des différents modèles
    """
    image_pixel = format_image(chemin) # Récupération des pixels de l'image
    image_pixel1d = image_pixel.reshape(1, 625) # Transformation en tableau 2D
    chemin_split = chemin.split("\\") # Split du chemin pour recupérer les informations
    
    # Prédiction des différents modèles
    predictions_type = model_type.predict(image_pixel1d)
    predictions_maj = model_maj.predict(image_pixel1d)
    predictions_min = model_min.predict(image_pixel1d)
    predictions_nbr = model_nbr.predict(image_pixel1d)
    
    # Get max value of predictions
    max_type = max(predictions_type[0]) # Type
    max_maj = max(predictions_maj[0]) # Maj
    max_min = max(predictions_min[0]) # Min
    max_nbr = max(predictions_nbr[0]) # Nbr
    
    # Dictionnaire des probabilités
    dictionnaire = {
        max(predictions_maj[0]): "MAJ",
        max(predictions_min[0]): "MIN",
        max(predictions_nbr[0]): "NBR"
    }
    
    # Get label type
    type_img = TYPE[tf.argmax(predictions_type, axis=1).numpy()[0]] # label type
    
    # Get label forme
    maximum_forme = max(max_maj, max_min, max_nbr) # probabilité forme
    forme = dictionnaire[maximum_forme] # label type
    if forme == "MAJ":
        label_max_forme = MAJ[tf.argmax(predictions_maj, axis=1).numpy()[0]]
    elif forme == "MIN":
        label_max_forme = MIN[tf.argmax(predictions_min, axis=1).numpy()[0]]
    elif forme == "NBR":
        label_max_forme = NBR[tf.argmax(predictions_nbr, axis=1).numpy()[0]]
    
    # JSON de retour pour l'API
    json_retour_api = {
        "Image": chemin,
        "Label": chemin_split[5],
        "Prediction": "",
        "Maj": predictions_type[0][0],
        "Min": predictions_type[0][1],
        "Nbr": predictions_type[0][2],
        "A": predictions_maj[0][0],
        "B": predictions_maj[0][1],
        "C": predictions_maj[0][2],
        "D": predictions_maj[0][3],
        "E": predictions_maj[0][4],
        "F": predictions_maj[0][5],
        "G": predictions_maj[0][6],
        "H": predictions_maj[0][7],
        "I": predictions_maj[0][8],
        "J": predictions_maj[0][9],
        "K": predictions_maj[0][10],
        "L": predictions_maj[0][11],
        "M": predictions_maj[0][12],
        "N": predictions_maj[0][13],
        "O": predictions_maj[0][14],
        "P": predictions_maj[0][15],
        "Q": predictions_maj[0][16],
        "R": predictions_maj[0][17],
        "S": predictions_maj[0][18],
        "T": predictions_maj[0][19],
        "U": predictions_maj[0][20],
        "V": predictions_maj[0][21],
        "W": predictions_maj[0][22],
        "X": predictions_maj[0][23],
        "Y": predictions_maj[0][24],
        "Z": predictions_maj[0][25],
        "a": predictions_min[0][0],
        "b": predictions_min[0][1],
        "c": predictions_min[0][2],
        "d": predictions_min[0][3],
        "e": predictions_min[0][4],
        "f": predictions_min[0][5],
        "g": predictions_min[0][6],
        "h": predictions_min[0][7],
        "i": predictions_min[0][8],
        "j": predictions_min[0][9],
        "k": predictions_min[0][10],
        "l": predictions_min[0][11],
        "m": predictions_min[0][12],
        "n": predictions_min[0][13],
        "o": predictions_min[0][14],
        "p": predictions_min[0][15],
        "q": predictions_min[0][16],
        "r": predictions_min[0][17],
        "s": predictions_min[0][18],
        "t": predictions_min[0][19],
        "u": predictions_min[0][20],
        "v": predictions_min[0][21],
        "w": predictions_min[0][22],
        "x": predictions_min[0][23],
        "y": predictions_min[0][24],
        "z": predictions_min[0][25],
        "0": predictions_nbr[0][0],
        "1": predictions_nbr[0][1],
        "2": predictions_nbr[0][2],
        "3": predictions_nbr[0][3],
        "4": predictions_nbr[0][4],
        "5": predictions_nbr[0][5],
        "6": predictions_nbr[0][6],
        "7": predictions_nbr[0][7],
        "8": predictions_nbr[0][8],
        "9": predictions_nbr[0][9]
    }
    
    # Choix de la prédiction finale 
    if type_img != forme:
        max_max_max = max(max_type, maximum_forme)
        if max_type == max_max_max:
            if type_img == "MAJ":
                json_retour_api["Prediction"] = MAJ[tf.argmax(predictions_maj, axis=1).numpy()[0]]
            elif type_img == "MIN":
                json_retour_api["Prediction"] = MIN[tf.argmax(predictions_min, axis=1).numpy()[0]]
            elif type_img == "NBR":
                json_retour_api["Prediction"] = NBR[tf.argmax(predictions_nbr, axis=1).numpy()[0]]
        else:
            json_retour_api["Prediction"] = label_max_forme
    else:
        json_retour_api["Prediction"] = label_max_forme
    
    return json_retour_api # Retourne le JSON

# Charger le dataset des images

@app.get("/predic")
async def predict_random():
    random_image = np.random.choice(CHEMAIN)
    json = predict_image(random_image)
    print("Label :", json["Label"])
    print("Prediction :", json["Prediction"])
    return predict_image(random_image)

