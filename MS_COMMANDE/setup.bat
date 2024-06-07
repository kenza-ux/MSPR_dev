@echo off

:: Créer un environnement virtuel
python -m venv env

:: Activer l'environnement virtuel
call env\Scripts\activate

:: Installer les dépendances depuis requirements.txt
pip install -r requirements.txt

:: Démarrer l'API Flask
python run.py
