"""Point d'entree WSGI pour les serveurs compatibles (production/classique)."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestion_produits.settings")

application = get_wsgi_application()
