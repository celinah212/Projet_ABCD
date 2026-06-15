"""Enregistrement des modeles dans l'interface d'administration Django."""

from django.contrib import admin

from .models import Categorie, Produit


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("nom",)
    search_fields = ("nom",)


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ("nom", "categorie", "prix", "quantite", "disponible", "date_creation")
    list_filter = ("categorie", "disponible")
    search_fields = ("nom", "description")
    ordering = ("-date_creation",)
