/* =========================================================================
   JavaScript vanilla pour le frontend de l'application.
   Aucun framework, aucun TypeScript, aucun JSX : uniquement du JS standard.
   ========================================================================= */

(function () {
    "use strict";

    // Cle utilisee dans localStorage pour memoriser le theme choisi.
    var THEME_STORAGE_KEY = "gestion-produits-theme";
    var THEME_DARK = "dark";
    var THEME_LIGHT = "light";

    // Attend que le DOM soit completement charge.
    document.addEventListener("DOMContentLoaded", function () {
        initTheme();
        initSettingsDropdown();
        initThemeToggle();
        initAboutModal();
        initWipeConfirmation();
        initAutoSubmitSurCategorie();
        initRechercheLive();
        initConfirmationSuppression();
        initMasquageMessages();
    });

    /**
     * Soumet automatiquement le formulaire de filtre lorsque l'utilisateur
     * change de categorie dans la liste deroulante.
     */
    function initAutoSubmitSurCategorie() {
        var select = document.getElementById("categorie-select");
        if (select && select.form) {
            select.addEventListener("change", function () {
                select.form.submit();
            });
        }
    }

    /**
     * Filtre les lignes du tableau en temps reel pendant la frappe,
     * en plus du filtrage cote serveur.
     */
    function initRechercheLive() {
        var input = document.getElementById("search-input");
        var table = document.getElementById("produits-table");
        if (!input || !table) {
            return;
        }

            var lignes = table.querySelectorAll("tbody tr");

            input.addEventListener("input", function () {
            var terme = input.value.toLowerCase().trim();
            var visibles = 0;

            lignes.forEach(function (ligne) {
                var nom = ligne.getAttribute("data-name") || "";
                var correspond = nom.indexOf(terme) !== -1;
                ligne.style.display = correspond ? "" : "none";
                if (correspond) {
                    visibles += 1;
                }
            });
        });
    }

    /**
     * Ajoute une confirmation cote client avant la suppression definitive.
     */
    function initConfirmationSuppression() {
        var formulaire = document.getElementById("delete-form");
        if (!formulaire) {
            return;
        }

        formulaire.addEventListener("submit", function (evenement) {
            var confirme = window.confirm(
                "Etes-vous sur de vouloir supprimer ce produit ? Cette action est irreversible."
            );
            if (!confirme) {
                evenement.preventDefault();
            }
        });
    }

    /**
     * Fait disparaitre les messages flash apres quelques secondes.
     */
    function initMasquageMessages() {
        var conteneur = document.getElementById("messages");
        if (!conteneur) {
            return;
        }

        window.setTimeout(function () {
            conteneur.style.opacity = "0";
            window.setTimeout(function () {
                if (conteneur.parentNode) {
                    conteneur.parentNode.removeChild(conteneur);
                }
            }, 400);
        }, 4000);
    }

    /**
     * Initialise le theme au chargement de la page a partir de localStorage.
     * Par defaut, le mode clair est utilise.
     */
    function initTheme() {
        var themeSauvegarde = lireTheme();
        appliquerTheme(themeSauvegarde);
    }

    /**
     * Lit le theme memorise. Retourne "light" si aucune valeur n'est presente.
     */
    function lireTheme() {
        try {
            var theme = window.localStorage.getItem(THEME_STORAGE_KEY);
            if (theme === THEME_DARK || theme === THEME_LIGHT) {
                return theme;
            }
        } catch (erreur) {
            // localStorage peut etre indisponible : on ignore silencieusement.
        }
        return THEME_LIGHT;
    }

    /**
     * Applique le theme courant au <html> et met a jour le libelle du bouton.
     */
    function appliquerTheme(theme) {
        var racine = document.documentElement;
        var libelle = document.getElementById("theme-label");

        if (theme === THEME_DARK) {
            racine.setAttribute("data-theme", THEME_DARK);
            if (libelle) {
                libelle.textContent = "Activer le mode clair";
            }
        } else {
            racine.removeAttribute("data-theme");
            if (libelle) {
                libelle.textContent = "Activer le mode sombre";
            }
        }
    }

    /**
     * Memorise le theme choisi dans localStorage.
     */
    function sauvegarderTheme(theme) {
        try {
            window.localStorage.setItem(THEME_STORAGE_KEY, theme);
        } catch (erreur) {
            // Ignore silencieusement si le stockage est indisponible.
        }
    }

    /**
     * Gere l'ouverture et la fermeture du menu deroulant Parametres.
     */
    function initSettingsDropdown() {
        var dropdown = document.getElementById("settings-dropdown");
        var bouton = document.getElementById("settings-button");
        if (!dropdown || !bouton) {
            return;
        }

        bouton.addEventListener("click", function (evenement) {
            evenement.stopPropagation();
            var ouvert = dropdown.classList.toggle("open");
            bouton.setAttribute("aria-expanded", ouvert ? "true" : "false");
        });

        // Ferme le menu si on clique ailleurs dans la page.
        document.addEventListener("click", function (evenement) {
            if (!dropdown.contains(evenement.target)) {
                dropdown.classList.remove("open");
                bouton.setAttribute("aria-expanded", "false");
            }
        });

        // Ferme le menu sur la touche Echap.
        document.addEventListener("keydown", function (evenement) {
            if (evenement.key === "Escape" && dropdown.classList.contains("open")) {
                dropdown.classList.remove("open");
                bouton.setAttribute("aria-expanded", "false");
                bouton.focus();
            }
        });
    }

    /**
     * Alterne entre le theme clair et le theme sombre au clic.
     */
    function initThemeToggle() {
        var bouton = document.getElementById("theme-toggle");
        if (!bouton) {
            return;
        }

        bouton.addEventListener("click", function () {
            var themeActuel = lireTheme();
            var nouveauTheme = themeActuel === THEME_DARK ? THEME_LIGHT : THEME_DARK;
            sauvegarderTheme(nouveauTheme);
            appliquerTheme(nouveauTheme);
        });
    }

    /**
     * Ouvre et ferme la modale A propos.
     */
    function initAboutModal() {
        var modale = document.getElementById("about-modal");
        var boutonOuvrir = document.getElementById("about-button");
        var boutonFermerHaut = document.getElementById("about-close");
        var boutonFermerBas = document.getElementById("about-close-footer");

        if (!modale || !boutonOuvrir) {
            return;
        }

        function ouvrir() {
            modale.removeAttribute("hidden");
            if (boutonFermerHaut) {
                boutonFermerHaut.focus();
            }
        }

        function fermer() {
            modale.setAttribute("hidden", "");
            boutonOuvrir.focus();
        }

        boutonOuvrir.addEventListener("click", ouvrir);

        if (boutonFermerHaut) {
            boutonFermerHaut.addEventListener("click", fermer);
        }
        if (boutonFermerBas) {
            boutonFermerBas.addEventListener("click", fermer);
        }

        // Ferme la modale en cliquant sur l'arriere-plan.
        modale.addEventListener("click", function (evenement) {
            if (evenement.target === modale) {
                fermer();
            }
        });

        // Ferme la modale sur la touche Echap.
        document.addEventListener("keydown", function (evenement) {
            if (evenement.key === "Escape" && !modale.hasAttribute("hidden")) {
                fermer();
            }
        });
    }

    /**
     * Demande une double confirmation avant de soumettre le formulaire
     * qui vide toute la base de donnees.
     */
    function initWipeConfirmation() {
        var formulaire = document.getElementById("wipe-form");
        if (!formulaire) {
            return;
        }

        formulaire.addEventListener("submit", function (evenement) {
            var premierAvertissement = window.confirm(
                "Voulez-vous vraiment vider toute la base de donnees ? " +
                "Tous les produits et toutes les categories seront supprimes."
            );
            if (!premierAvertissement) {
                evenement.preventDefault();
                return;
            }

            var secondAvertissement = window.confirm(
                "Derniere confirmation : cette operation est IRREVERSIBLE. " +
                "Poursuivre ?"
            );
            if (!secondAvertissement) {
                evenement.preventDefault();
            }
        });
    }
})();
