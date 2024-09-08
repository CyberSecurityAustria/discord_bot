# Verwende ein offizielles Python-Image als Basis
FROM python:3.9-slim

# Setze ein Arbeitsverzeichnis
WORKDIR /usr/src/app

# Kopiere das requirements.txt in das Arbeitsverzeichnis
COPY requirements.txt ./

# Installiere Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest des Projektverzeichnisses in das Arbeitsverzeichnis
COPY . .

# Exponiere den Port (optional, falls du Flask oder andere Webservices verwendest)
# EXPOSE 5000

# Startet den Bot
CMD ["python", "./main.py"]
