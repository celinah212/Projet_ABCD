"""
Vues de l'application (couche "View" du MVT).

Vues fonctionnelles implementant le CRUD complet :
  - liste_produits        : READ (liste + recherche + filtre)
  - detail_produit        : READ (fiche detaillee)
  - nouveau_produit       : CREATE
  - modifier_produit      : UPDATE
  - supprimer_produit     : DELETE (avec confirmation)
"""

from django.contrib import messages
from django.core.paginator import Paginator
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProduitForm
from .models import Categorie, Produit

PRODUITS_PAR_PAGE = 10


def liste_produits(request):
    """Affiche la liste paginee des produits (10 par page) avec recherche."""
    query = request.GET.get("q", "").strip()
    categorie_id = request.GET.get("categorie", "").strip()

    produits = Produit.objects.select_related("categorie").all()

    if query:
        produits = produits.filter(nom__icontains=query)
    if categorie_id:
        produits = produits.filter(categorie_id=categorie_id)

    total = produits.count()
    paginator = Paginator(produits, PRODUITS_PAR_PAGE)

    page_obj = paginator.get_page(request.GET.get("page"))

    categories = Categorie.objects.all()

    return render(
        request,
        "produits/liste_produits.html",
        {
            "page_obj": page_obj,
            "produits": page_obj.object_list,
            "categories": categories,
            "query": query,
            "categorie_selectionnee": categorie_id,
            "total": total,
        },
    )


def detail_produit(request, pk):
    """Affiche le detail d'un produit."""
    produit = get_object_or_404(Produit, pk=pk)
    return render(request, "produits/detail_produit.html", {"produit": produit})


def nouveau_produit(request):
    """Cree un nouveau produit (GET = formulaire vide, POST = enregistrement)."""
    if request.method == "POST":
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le produit a ete cree avec succes.")
            return redirect("produits:liste_produits")
    else:
        form = ProduitForm()

    return render(
        request,
        "produits/form_produit.html",
        {"form": form, "titre": "Ajouter un produit", "bouton": "Creer le produit"},
    )


def modifier_produit(request, pk):
    """Modifie un produit existant."""
    produit = get_object_or_404(Produit, pk=pk)

    if request.method == "POST":
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, "Le produit a ete modifie avec succes.")
            return redirect("produits:liste_produits")
    else:
        form = ProduitForm(instance=produit)

    return render(
        request,
        "produits/form_produit.html",
        {
            "form": form,
            "produit": produit,
            "titre": "Modifier le produit",
            "bouton": "Enregistrer les modifications",
        },
    )


def supprimer_produit(request, pk):
    """Supprime un produit apres confirmation (GET = confirmation, POST = delete)."""
    produit = get_object_or_404(Produit, pk=pk)

    if request.method == "POST":
        produit.delete()
        messages.success(request, "Le produit a ete supprime avec succes.")
        return redirect("produits:liste_produits")

    return render(request, "produits/confirmer_suppression.html", {"produit": produit})


def vider_base(request):
    """
    Supprime tous les produits et toutes les categories de la base.
    Uniquement accessible en POST pour eviter toute suppression accidentelle.
    Redirige toujours vers la liste des produits apres execution.
    """
    if request.method != "POST":
        messages.error(
            request,
            "Cette action doit etre declenchee depuis un formulaire.",
        )
        return redirect("produits:liste_produits")

    nb_produits = Produit.objects.count()
    nb_categories = Categorie.objects.count()

    # Ordre important : on supprime d'abord les produits car ils referencent
    # la categorie via une cle etrangere.
    Produit.objects.all().delete()
    Categorie.objects.all().delete()

    messages.success(
        request,
        "Base de donnees videe : {} produit(s) et {} categorie(s) supprimes.".format(
            nb_produits, nb_categories
        ),
    )
    return redirect("produits:liste_produits")


def gerer_categories(request):
    """
    Affiche la liste des categories et permet d'en ajouter une nouvelle.
    POST = creation. GET = affichage du formulaire et de la liste.
    """
    if request.method == "POST":
        nom = request.POST.get("nom", "").strip()
        if not nom:
            messages.error(request, "Le nom de la categorie est obligatoire.")
        elif Categorie.objects.filter(nom__iexact=nom).exists():
            messages.error(
                request,
                "Une categorie portant ce nom existe deja.",
            )
        else:
            Categorie.objects.create(nom=nom)
            messages.success(
                request,
                "La categorie '{}' a ete creee avec succes.".format(nom),
            )

        # Redirection pour eviter la re-soumission du formulaire.
        return redirect("produits:gerer_categories")

    categories = Categorie.objects.annotate(
        nb_produits=models.Count("produit")
    ).order_by("nom")

    return render(
        request,
        "produits/gerer_categories.html",
        {"categories": categories},
    )


def supprimer_categorie(request, pk):
    """
    Supprime une categorie identifiee par sa cle primaire.
    Les produits lies conservent leurs autres informations (on_delete=SET_NULL).
    """
    categorie = get_object_or_404(Categorie, pk=pk)

    if request.method != "POST":
        messages.error(
            request,
            "La suppression doit etre declenchee depuis un formulaire.",
        )
        return redirect("produits:gerer_categories")

    nom = categorie.nom
    categorie.delete()
    messages.success(
        request,
        "La categorie '{}' a ete supprimee. Les produits associes ne sont plus classes.".format(
            nom
        ),
    )
    return redirect("produits:gerer_categories")
