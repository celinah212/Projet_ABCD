"""
Configuration principale des URLs du projet gestion_produits.

Aucune route d'authentification (login) n'est definie : l'application
de gestion des produits est accessible directement.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Toutes les routes de l'application "produits" sont prefixees par "/".
    path("", include("produits.urls")),
]
