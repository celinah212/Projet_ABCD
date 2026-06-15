"""
URLs de l'application produits.

Chaque route est nommee pour pouvoir utiliser {% url 'produits:...' %}
dans les templates et reverse() dans le code Python.
"""

from django.urls import path

from . import views

app_name = "produits"

urlpatterns = [
    path("", views.liste_produits, name="liste_produits"),
    path("produit/<int:pk>/", views.detail_produit, name="detail_produit"),
    path("nouveau/", views.nouveau_produit, name="nouveau_produit"),
    path("modifier/<int:pk>/", views.modifier_produit, name="modifier_produit"),
    path("supprimer/<int:pk>/", views.supprimer_produit, name="supprimer_produit"),
    path("parametres/vider-base/", views.vider_base, name="vider_base"),
    path("parametres/categories/", views.gerer_categories, name="gerer_categories"),
    path("parametres/categories/supprimer/<int:pk>/", views.supprimer_categorie, name="supprimer_categorie"),
]
