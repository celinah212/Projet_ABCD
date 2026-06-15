"""
Formulaires bases sur les modeles (couche de validation des donnees).

On utilise un ModelForm pour generer et valider le formulaire du produit
a partir du modele, en controlant les widgets pour le rendu HTML/CSS.
"""

from django import forms

from .models import Produit


class ProduitForm(forms.ModelForm):
    """Formulaire de creation et de modification d'un produit."""

    class Meta:
        model = Produit
        fields = ["nom", "description", "prix", "quantite", "categorie", "disponible"]
        widgets = {
            "nom": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ex. Clavier mecanique"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "Description du produit"}
            ),
            "prix": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "min": "0", "placeholder": "Montant en Ariary"}
            ),
            "quantite": forms.NumberInput(
                attrs={"class": "form-control", "min": "0"}
            ),
            "categorie": forms.Select(attrs={"class": "form-control"}),
            "disponible": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_nom(self):
        """Le nom ne doit pas etre vide apres nettoyage des espaces."""
        nom = self.cleaned_data.get("nom", "").strip()
        if not nom:
            raise forms.ValidationError("Le nom du produit est obligatoire.")
        return nom
