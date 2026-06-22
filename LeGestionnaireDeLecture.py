"""
KATA PYTHON #050 - Le Gestionnaire de Lecture
Difficulté : 3/10

ÉNONCÉ :
Vous devez créer une classe `Livre` qui permet de suivre la progression de
lecture d'un ouvrage.

On vous demande de compléter la classe `Livre` ci-dessous.

RÈGLES ET CONTRAINTES :
1. L'initialisation (`__init__`) prend trois paramètres : `titre` (str),
   `auteur` (str) et `total_pages` (int).
   Un quatrième attribut nommé `page_actuelle` doit être initialisé à 0 (il ne
   fait pas partie des paramètres du `__init__`).
2. La méthode `avancer_lecture(nombre_pages)` ajoute le nombre de pages lues
   à `page_actuelle`.
   - Si la progression dépasse `total_pages`, `page_actuelle` doit être bloquée
     au maximum (égal à `total_pages`).
3. La méthode `est_termine()` renvoie un booléen (`True` si le livre est
   complètement lu, `False` sinon).
4. La méthode spéciale `__str__(self)` doit renvoyer une chaîne de caractères
   au format exact : "TITRE par AUTEUR (PAGE_ACTUELLE/TOTAL_PAGES)"
   Exemple : "Le Petit Prince par Antoine de Saint-Exupéry (45/90)"
"""

import unittest


class Livre:
    """Représente un livre et suit sa progression de lecture."""

    def __init__(self, titre: str, auteur: str, total_pages: int):
        """Initialise un livre avec son titre, auteur et le nombre total de pages."""
        # TODO: Initialiser titre, auteur, total_pages et page_actuelle (à 0)
        pass

    def avancer_lecture(self, nombre_pages: int) -> None:
        """Avance le marque-page du nombre de pages lues sans dépasser le total."""
        # TODO: Implémenter la logique de progression
        pass

    def est_termine(self) -> bool:
        """Indique si le livre a été entièrement lu."""
        # TODO: Retourner le booléen correspondant
        pass

    def __str__(self) -> str:
        """Renvoie la représentation textuelle de l'état du livre."""
        # TODO: Retourner la chaîne formatée demandée
        pass


# =====================================================================
# TESTS UNITAIRES (Ne pas modifier cette section)
# =====================================================================


class TestGestionnaireLivre(unittest.TestCase):
    """Suite de tests pour valider la classe Livre."""

    def test_initialisation(self):
        """Vérifie que les attributs de départ sont correctement configurés."""
        livre = Livre("Dune", "Frank Herbert", 600)
        self.assertEqual(
            livre.titulaire if hasattr(livre, "titulaire") else livre.titre, "Dune"
        )
        self.assertEqual(livre.auteur, "Frank Herbert")
        self.assertEqual(livre.total_pages, 600)
        self.assertEqual(livre.page_actuelle, 0)

    def test_avancer_lecture_standard(self):
        """Vérifie qu'on avance correctement dans le livre."""
        livre = Livre("1984", "George Orwell", 300)
        livre.avancer_lecture(50)
        self.assertEqual(livre.page_actuelle, 50)
        self.assertFalse(livre.est_termine())

    def test_avancer_lecture_limite(self):
        """La progression ne doit pas pouvoir dépasser le nombre total de pages."""
        livre = Livre("Le Hobbit", "J.R.R. Tolkien", 300)
        livre.avancer_lecture(350)  # On lit plus que le total
        self.assertEqual(livre.page_actuelle, 300)
        self.assertTrue(livre.est_termine())

    def test_affichage_str(self):
        """Vérifie le format de la méthode magique __str__."""
        livre = Livre("Fondation", "Isaac Asimov", 250)
        livre.avancer_lecture(100)

        attendu = "Fondation par Isaac Asimov (100/250)"
        self.assertEqual(str(livre), attendu)


if __name__ == "__main__":
    unittest.main(verbosity=2)
