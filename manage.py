#!/usr/bin/env python
"""Outil de gestion en ligne de commande pour le projet gestion_produits."""
import os
import sys


def main():
    """Point d'entree des commandes administratives Django."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestion_produits.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django n'est pas installe. Activez votre environnement virtuel "
            "puis lancez : pip install -r requirements.txt"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
