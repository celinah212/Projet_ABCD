"""Filtres et tags personnalises pour les templates de l'application produits."""

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, field, value):
    """
    Renvoie la chaine de requete courante dans laquelle le parametre ``field``
    est remplace par ``value`` (ou ajoute si absent).

    Exemple d'utilisation dans un template :
        <a href="?{% url_replace request 'page' 3 %}">Page 3</a>
    """
    request = context.get("request")
    if request is None:
        return ""

    parametres = request.GET.copy()
    parametres[field] = value
    return parametres.urlencode()
