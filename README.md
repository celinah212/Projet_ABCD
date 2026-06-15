# Gestion de produits (CRUD) - Django MVT

Application de gestion de produits realisee avec le framework Django en
respectant l'architecture **MVT** (Model - View - Template), equivalente du
pattern MVC adapte a Django.

Le CRUD complet est implemente : **C**reate, **R**ead, **U**pdate, **D**elete.

## Choix techniques

- Backend : Django (Python), architecture MVT.
- Frontend : HTML + CSS + JavaScript vanilla
- Templates : moteur de templates Django (cote serveur).
- Base de donnees : SQLite (incluse, aucune configuration requise).


## Structure des dossiers

```
gestion_produits/                  # racine du projet (contient manage.py)
|-- manage.py                      # utilitaire de ligne de commande Django
|-- requirements.txt               # dependances Python
|-- db.sqlite3                     # base de donnees (generee apres migrate)
|
|-- gestion_produits/              # paquet de configuration du projet
|   |-- __init__.py
|   |-- settings.py                # parametres du projet
|   |-- urls.py                    # routes principales
|   |-- wsgi.py                    # point d'entree WSGI
|   `-- asgi.py                    # point d'entree ASGI
|
|-- produits/                      # application (le coeur du projet)
|   |-- __init__.py
|   |-- apps.py                    # configuration de l'application
|   |-- models.py                  # MODEL    : Categorie, Produit
|   |-- forms.py                   # formulaires bases sur les modeles
|   |-- views.py                   # VIEW     : logique CRUD
|   |-- admin.py                   # configuration de l'admin Django
|   |-- urls.py                    # routes de l'application
|   |-- migrations/
|   |   |-- __init__.py
|   |   `-- 0001_initial.py        # schema de base de donnees
|   |-- management/
|   |   `-- commands/
|   |       |-- __init__.py
|   |       `-- seed_db.py         # commande de donnees de demonstration
|   `-- templates/
|       `-- produits/
|           |-- base.html          # TEMPLATE : squelette commun
|           |-- liste_produits.html
|           |-- detail_produit.html
|           |-- form_produit.html
|           `-- confirmer_suppression.html
|
`-- static/                        # fichiers statiques du frontend
    |-- css/
    |   `-- style.css
    `-- js/
        `-- main.js                # JavaScript vanilla
```

### Correspondance MVC / MVT

| Patron classique (MVC) | Equivalent Django (MVT)        |
|------------------------|--------------------------------|
| Model                  | `produits/models.py`           |
| View (logique)         | `produits/views.py`            |
| Template (presentation)| `produits/templates/`          |
| Controller (routes)    | `produits/urls.py`             |

## Installation et lancement

1. Placer le dossier `gestion_produits` sur la machine et s'y placer :
   ```
   cd gestion_produits
   ```

2. (Optionnel mais recommande) Creer et activer un environnement virtuel :
   ```
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. Installer les dependances :
   ```
   pip install -r requirements.txt
   ```

4. Appliquer les migrations pour creer la base de donnees :
   ```
   python manage.py migrate
   python manage.py makemigrations produits
   python manage.py migrate
   ```

5. (Optionnel) Generer des donnees de demonstration :
   ```
   python manage.py seed_db
   ```

6. Lancer le serveur de developpement :
   ```
   python manage.py runserver
   ```

7. Ouvrir le navigateur a l'adresse : http://127.0.0.1:8000/

## Routes disponibles

| URL                       | Action                                 |
|---------------------------|----------------------------------------|
| `/`                       | Liste des produits (recherche + filtre)|
| `/produit/<id>/`          | Fiche detaillee d'un produit           |
| `/nouveau/`               | Formulaire de creation                 |
| `/modifier/<id>/`         | Formulaire de modification             |
| `/supprimer/<id>/`        | Confirmation de suppression            |

## Fonctionnalites cote frontend (JavaScript vanilla)

- Recherche instantanee dans le tableau pendant la frappe.
- Soumission automatique du filtre lors du changement de categorie.
- Confirmation supplementaire avant toute suppression.
- Disparition automatique des messages d'information apres quelques secondes.

## Autres fonctionnalites

- **Menu Parametres** dans l'en-tete : bascule du theme clair/sombre, gestion
  des categories, option de reinitialisation de la base, fenetre "A propos".
- **Pagination** des produits par 10 sur la page principale (Django Paginator).
- **Gestion des categories** : creation et suppression directe depuis une page
  dediee accessible via le menu Parametres.
- **Devise** : les prix sont exprimes en **Ariary** dans toute l'application.
