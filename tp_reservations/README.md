# TP : API de réservation de salles

Auteur : Enow Eweh Mac Brenda (travail individuel)

## Installation

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed
python manage.py runserver

Comptes de test : alice, bob, charlie (motdepasse123). Super-utilisateur : admin / admin123.

## Endpoints

| Route | Methodes | Permissions |
|-------|----------|-------------|
| /api/salles/ | GET, POST | lecture pour tous, ecriture admin |
| /api/salles/{id}/ | GET, PUT, PATCH, DELETE | lecture pour tous, ecriture admin |
| /api/reservations/ | GET, POST | lecture pour tous, creation par un utilisateur connecte |
| /api/reservations/{id}/ | GET, PUT, PATCH, DELETE | modification et suppression par l'auteur seulement |
| /api/salles/{id}/occupation/ | GET | parametres debut et fin au format ISO 8601 |

## Choix de conception et difficultes

Pour le chevauchement, je regarde si le debut ou la fin d'une reservation deja confirmee de la
meme salle tombe dans l'intervalle de la nouvelle reservation. Si un des deux tombe dedans, il y a
chevauchement. Deux reservations qui se touchent (l'une finit a 10h et l'autre commence a 10h) ne se
chevauchent pas, et une reservation annulee ne bloque rien.

Pour l'occupation je prends seulement les reservations CONFIRMEE et je ne compte que la partie qui
se trouve dans la periode demandee, puis je divise par la duree de la periode.

Difficulte : les champs absents en PATCH, et le decoupage des reservations qui depassent la periode.
