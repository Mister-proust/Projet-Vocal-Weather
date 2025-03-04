Pour lancer l'application, veuillez vous rendre avec votre invite de commande dans le dossier App-vocal-weather puis écrivez dans le terminal : 
uvicorn main:app --reload  
fastapi dev main.py

Nécessité d'installer FFmpeg et de le mettre dans un path via vos paramètres avancées --> Variables d'environnement --> Path --> Mettre le chemin ou vous avez installer FFmpeg

Pour faire fonctionner l'appli une fois ouverte, cliquez sur le bouton microphone violet et demandé la météo souhaitée tout en sachant qu'elle est limitée à J+3. 