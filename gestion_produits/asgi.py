"""Point d'entree ASGI pour les serveurs asynchrones."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestion_produits.settings")

application = get_asgi_application()
