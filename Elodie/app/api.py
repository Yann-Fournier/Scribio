from fastapi import FastAPI
import tensorflow as tf
import numpy as np
from PIL import Image
from pydantic import BaseModel
import json
import os # to work with directories
import json # to work with json files
import tensorflow as tf # deep learning library. Tensors are just multi-dimensional arrays
import numpy as np # linear algebra
from PIL import Image # image processing
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from awscli.customizations.s3.utils import relative_path

app = FastAPI()


# Autoriser les requêtes depuis React (http://localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser toutes les origines (ou préciser ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les headers
)

# Chargement des modèles
model_type = tf.keras.models.load_model("../../Yann/models/Get_Type_v4_b32_e10.keras")
model_maj = tf.keras.models.load_model("../../Yann/models/Get_Maj_v4_b32_e10.keras")
model_min = tf.keras.models.load_model("../../Yann/models/Get_Min_v4_b32_e10.keras")
model_nbr = tf.keras.models.load_model("../../Yann/models/Get_Nbr_v4_b32_e10.keras")

# Dictionnaires de correspondance
TYPE = {0: 'MAJ', 1: 'MIN', 2: 'NBR'}
MAJ = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'}
MIN = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z'}
NBR = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9'}
CHEMAIN = []

# # Classe pour recevoir les données
# class ImageData(BaseModel):
#     image_path: str  # Le chemin de l'image

# Fonction pour traiter l'image
from fastapi.staticfiles import StaticFiles

# Monter le dossier Dataset comme serveur de fichiers statiques
app.mount("/static", StaticFiles(directory="../../Dataset"), name="static")

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
# Fonction principale pour prédire l'image

import boto3

s3 = boto3.client('s3')

# Liste des buckets à parcourir
buckets = ['scribio1', 'scribio2', 'scribio3']
#buckets = ['test354680'] ###Test avec un seul bucket qui contient que des majuscules et tres peux de fichiers
local_folder ={
    'majuscules': '../../Majuscules',
    'minuscules': '../../Minuscules',
    'digits': '../../Digits'
}
for folder in local_folder.values():
    os.makedirs(folder, exist_ok=True)
    
CHEMIN = []

def download_from_s3(s3_path: str, prefix: str = '') -> None:
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter='/')
    
    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            if key.lower().endswith('.png'):
                file_name = os.path.basename(key)
                relative_path = os.path.dirname(key)
                parent_folder = os.path.basename(relative_path)
                category =None 
                
                if parent_folder.isupper():
                    category = 'majuscules'
                elif parent_folder.islower():
                    category = 'minuscules'
                elif parent_folder.isdigit():
                    category = 'digits'
            
                if category:
                    local_subfolder = os.path.join(local_folder[category], relative_path)
                    os.makedirs(local_subfolder, exist_ok=True)
                    local_path = os.path.join(local_subfolder, file_name)
                    s3.download_file(bucket, key, local_path)
                    CHEMIN.append(local_path)
    if 'CommonPrefixes' in response:
        for folder in response['CommonPrefixes']:
            download_from_s3(bucket, folder['Prefix'])

for bucket in buckets:
    print(f"Downloading from bucket {bucket} ...")
    download_from_s3(bucket)

print("Chemins des fichiers téléchargés :")
for chemin in CHEMIN:
    print(chemin)

# Parcours des dossiers et sous-dossiers pour récupérer les chemins de toutes les photos (recursion)
# def recup_chemin(chemin: str) -> None:
#     """Summary ______________________________________________________________

#     Args:
#         chemin (str): chemin du dataset
#     """
#     dossiers = [f for f in os.listdir(chemin) if os.path.isdir(os.path.join(chemin, f))]
#     if len(dossiers) == 0: # Si aucun dossier n'est trouvé, on est dans le cas de base
#         fichiers_png = [os.path.join(chemin, f) for f in os.listdir(chemin) if f.endswith('.png')] # on recupère et stocke les fichiers .png
#         CHEMAIN.extend(fichiers_png) # on ajoute les chemins des fichiers .png dans une liste
#     else : # Sinon, on continue de parcourir les dossiers
#         for dossier in dossiers:
#             recup_chemin(os.path.join(chemin, dossier))

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
    label = chemin_split[-2] if len(chemin_split) > 1 else "Inconnu"  # Le dossier parent est à l'avant-dernière position
    
    # Prédiction des différents modèles
    predictions_type = model_type.predict(image_pixel1d)
    predictions_maj = model_maj.predict(image_pixel1d)
    predictions_min = model_min.predict(image_pixel1d)
    predictions_nbr = model_nbr.predict(image_pixel1d)
    
    print(predictions_type)
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
 
    type_img = TYPE[int(tf.argmax(predictions_type, axis=1).numpy()[0])] # label type
    
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
        "Label": label,
        "Prediction": "",
        "Maj": float(predictions_type[0][0]),
        "Min": float(predictions_type[0][1]),
        "Nbr": float(predictions_type[0][2]),
        "A": float(predictions_maj[0][0]),
        "B": float(predictions_maj[0][1]),
        "C": float(predictions_maj[0][2]),
        "D": float(predictions_maj[0][3]),
        "E": float(predictions_maj[0][4]),
        "F": float(predictions_maj[0][5]),
        "G": float(predictions_maj[0][6]),
        "H": float(predictions_maj[0][7]),
        "I": float(predictions_maj[0][8]),
        "J": float(predictions_maj[0][9]),
        "K": float(predictions_maj[0][10]),
        "L": float(predictions_maj[0][11]),
        "M": float(predictions_maj[0][12]),
        "N": float(predictions_maj[0][13]),
        "O": float(predictions_maj[0][14]),
        "P": float(predictions_maj[0][15]),
        "Q": float(predictions_maj[0][16]),
        "R": float(predictions_maj[0][17]),
        "S": float(predictions_maj[0][18]),
        "T": float(predictions_maj[0][19]),
        "U": float(predictions_maj[0][20]),
        "V": float(predictions_maj[0][21]),
        "W": float(predictions_maj[0][22]),
        "X": float(predictions_maj[0][23]),
        "Y": float(predictions_maj[0][24]),
        "Z": float(predictions_maj[0][25]),
        "a": float(predictions_min[0][0]),
        "b": float(predictions_min[0][1]),
        "c": float(predictions_min[0][2]),
        "d": float(predictions_min[0][3]),
        "e": float(predictions_min[0][4]),
        "f": float(predictions_min[0][5]),
        "g": float(predictions_min[0][6]),
        "h": float(predictions_min[0][7]),
        "i": float(predictions_min[0][8]),
        "j": float(predictions_min[0][9]),
        "k": float(predictions_min[0][10]),
        "l": float(predictions_min[0][11]),
        "m": float(predictions_min[0][12]),
        "n": float(predictions_min[0][13]),
        "o": float(predictions_min[0][14]),
        "p": float(predictions_min[0][15]),
        "q": float(predictions_min[0][16]),
        "r": float(predictions_min[0][17]),
        "s": float(predictions_min[0][18]),
        "t": float(predictions_min[0][19]),
        "u": float(predictions_min[0][20]),
        "v": float(predictions_min[0][21]),
        "w": float(predictions_min[0][22]),
        "x": float(predictions_min[0][23]),
        "y": float(predictions_min[0][24]),
        "z": float(predictions_min[0][25]),
        "0": float(predictions_nbr[0][0]),
        "1": float(predictions_nbr[0][1]),
        "2": float(predictions_nbr[0][2]),
        "3": float(predictions_nbr[0][3]),
        "4": float(predictions_nbr[0][4]),
        "5": float(predictions_nbr[0][5]),
        "6": float(predictions_nbr[0][6]),
        "7": float(predictions_nbr[0][7]),
        "8": float(predictions_nbr[0][8]),
        "9": float(predictions_nbr[0][9])
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



# Endpoint API pour faire une prédiction
@app.on_event("startup")  # Charge les chemins au démarrage du serveur
def load_images():
    global CHEMAIN
    download_from_s3(bucket)
    print(f"✅ {len(CHEMAIN)} images trouvées !")



@app.post("/predict")
async def predict(request: Request):
    print(f"Requête reçue : {request.method} {request.url}")  # Log la requête

    if not CHEMAIN:
        return {"error": "Aucune image trouvée dans le dataset."}

    # random_image = np.random.choice(CHEMAIN)
    # json_result = predict_image(random_image)

    fichier_aleatoire = np.random.choice(CHEMIN)
    print(f"Fichier sélectionné au hasard : {fichier_aleatoire}")


    json = predict_image(fichier_aleatoire)

    # Retourner également l'URL du chemin de l'image

    return json
