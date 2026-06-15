"""
Commande personnalisee : python manage.py seed_db

Cree des categories et des produits de demonstration si la base est vide.
Idempotente : relancer la commande n'ajoute pas de doublons.
"""

from django.core.management.base import BaseCommand

from produits.models import Categorie, Produit


CATEGORIES = [
    "Electronique",
    "Alimentation",
    "Vetements",
    "Livres",
    "Maison",
]

PRODUITS = [
    {
        "nom": "Clavier mecanique",
        "description": "Clavier filaire retro-eclaire avec commutateurs bleus.",
        "prix": "79.90",
        "quantite": 25,
        "categorie": "Electronique",
        "disponible": True,
    },
    {
        "nom": "Souris sans fil",
        "description": "Souris ergonomique avec capteur optique haute precision.",
        "prix": "24.50",
        "quantite": 60,
        "categorie": "Electronique",
        "disponible": True,
    },
    {
        "nom": "Cafe en grains 1kg",
        "description": "Melange d'arabica torrefie, intensite moyenne.",
        "prix": "18.00",
        "quantite": 120,
        "categorie": "Alimentation",
        "disponible": True,
    },
    {
        "nom": "T-shirt coton",
        "description": "T-shirt unisexe, 100% coton biologique.",
        "prix": "15.90",
        "quantite": 0,
        "categorie": "Vetements",
        "disponible": False,
    },
    {
        "nom": "Roman d'aventure",
        "description": "Best-seller de la rentree litteraire, edition brochee.",
        "prix": "12.30",
        "quantite": 40,
        "categorie": "Livres",
        "disponible": True,
    },
    {
        "nom": "Lampe de bureau LED",
        "description": "Lampe a intensite reglable et port USB integre.",
        "prix": "34.99",
        "quantite": 15,
        "categorie": "Maison",
        "disponible": True,
    },
]


class Command(BaseCommand):
    help = "Cree des categories et des produits de demonstration."

    def handle(self, *args, **options):
        categories_creees = 0
        categorie_objets = {}

        for nom in CATEGORIES:
            obj, created = Categorie.objects.get_or_create(nom=nom)
            categorie_objets[nom] = obj
            if created:
                categories_creees += 1

        produits_crees = 0
        for donnees in PRODUITS:
            obj, created = Produit.objects.get_or_create(
                nom=donnees["nom"],
                defaults={
                    "description": donnees["description"],
                    "prix": donnees["prix"],
                    "quantite": donnees["quantite"],
                    "categorie": categorie_objets[donnees["categorie"]],
                    "disponible": donnees["disponible"],
                },
            )
            if created:
                produits_crees += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Donnees creees : {} categorie(s), {} produit(s).".format(
                    categories_creees, produits_crees
                )
            )
        )
