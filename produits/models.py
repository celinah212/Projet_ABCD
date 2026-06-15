"""
Modeles de l'application (couche "Model" du MVT).

Deux modeles :
  - Categorie : regroupe les produits par theme.
  - Produit   : l'element principal gere en CRUD.
"""

from django.db import models


class Categorie(models.Model):
    """Une categorie de produits (ex. Electronique, Alimentation...)."""

    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom")

    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categories"
        ordering = ["nom"]

    def __str__(self):
        return self.nom


class Produit(models.Model):
    """Produit gere par l'application (Create, Read, Update, Delete)."""

    nom = models.CharField(max_length=200, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    prix = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Prix (Ariary)"
    )
    quantite = models.PositiveIntegerField(default=0, verbose_name="Quantite en stock")
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Categorie",
    )
    disponible = models.BooleanField(default=True, verbose_name="Disponible")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de creation")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ["-date_creation"]

    def __str__(self):
        return self.nom

    @property
    def valeur_stock(self):
        """Valeur totale du stock pour ce produit (prix * quantite)."""
        return self.prix * self.quantite
