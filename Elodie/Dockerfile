# Étape 1 : Utiliser une image Python officielle comme base
FROM python:3.9

# Étape 2 : Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Étape 3 : Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Étape 4 : Copier les fichiers main.py et my_interface.py dans le conteneur
COPY app/main.py /app/main.py
COPY app/my_interface.py /app/my_interface.py

# Étape 5 : Exposer le port 80
EXPOSE 80

# Étape 6 : Lancer les deux scripts Python en parallèle
CMD ["sh", "-c", "python /app/main.py & python /app/my_interface.py"]
