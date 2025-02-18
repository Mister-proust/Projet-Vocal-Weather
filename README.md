# Projet-Vocal-Weather
Projet réalisé dans le cadre de la formation Développeur en Intelligence Artificielle.

# Version python
Obligation absolue de travailler sous python 3.12

## Installation

1.  Création de l'environnement virtuel

```bash
python3 -m venv env
```

2. Activation de l'environnement virtuel

```bash
# Linux/MacOS
source env/bin/activate

# Windows
env\Scripts\activate
```

3. Installation des dépendances

```bash
pip install -r requirements.txt
```

4. Connexion à la base de données et fichier caché

Les paramètres de connexion à la base de données ainsi que les données sensibles doivent être mises dans un fichier ```.env```.

```
# fichier .env

DB_HOST="database_host"
DB_PORT="server_port"
DB_USER="username"
DB_PASS="password"
DB_NAME="database_name"

SPEECH_KEY = "YourKey"
SPEECH_REGION = "YourRegion"
YOUR_API_KEY = "YourAPIWeatherKey"
```