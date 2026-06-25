"""
KATA PYTHON #049 - Le Filtrage Temporel (Fonctions Lambda)
Difficulté : 4/10

ÉNONCÉ :
On vous fournit une liste de dictionnaires représentant des événements
historiques ou des tâches. Chaque événement possède un "nom" (str) et
une "annee" (int) qui peut être négative (pour l'avant J.-C.).

On vous demande de compléter trois fonctions différentes.
CONTRAINTE MAJEURE : Vous devez obligatoirement utiliser une fonction `lambda`
à l'intérieur de chacune d'elles.

1. `extraire_annees(evenements)` : Renvoie une liste contenant uniquement les
   années de chaque événement (Indice : utilisez `map()`).
2. `filtrer_avant_jc(evenements)` : Renvoie une sous-liste contenant uniquement
   les événements dont l'année est strictement inférieure à 0 (Indice : utilisez `filter()`).
3. `trier_par_annee(evenements)` : Renvoie une nouvelle liste d'événements
   triés du plus ancien au plus récent (Indice : utilisez `sorted()` et son argument `key`).
"""

import unittest


def extraire_annees(evenements: list[dict]) -> list[int]:
    """Extrait et retourne la liste de toutes les années des événements."""
    return list(map(lambda x: x["annee"], evenements))


def filtrer_avant_jc(evenements: list[dict]) -> list[dict]:
    """Retourne uniquement les événements ayant eu lieu avant l'an 0 (année < 0)."""
    return list(filter(lambda x: x["annee"] < 0, evenements))


def trier_par_annee(evenements: list[dict]) -> list[dict]:
    """Retourne une nouvelle liste d'événements triés par ordre chronologique."""
    return list(sorted(evenements, key=lambda x: x["annee"]))


# =====================================================================
# TESTS UNITAIRES (Ne pas modifier cette section)
# =====================================================================


class TestLambdaOperations(unittest.TestCase):
    """Suite de tests pour valider les fonctions utilisant des lambdas."""

    def setUp(self):
        """Initialisation du jeu de données."""
        self.DATA = [
            {"nom": "Chute de Rome", "annee": 476},
            {"nom": "Fondation de Rome", "annee": -753},
            {"nom": "Bataille de Marignan", "annee": 1515},
            {"nom": "Construction des Pyramides de Gizeh", "annee": -2560},
            {"nom": "Premier pas sur la Lune", "annee": 1969},
        ]

    def test_extraire_annees(self):
        """Doit extraire correctement toutes les années dans l'ordre d'origine."""
        attendu = [476, -753, 1515, -2560, 1969]
        self.assertEqual(extraire_annees(self.DATA), attendu)

    def test_filtrer_avant_jc(self):
        """Doit isoler uniquement les deux événements avant l'an 0."""
        attendu = [
            {"nom": "Fondation de Rome", "annee": -753},
            {"nom": "Construction des Pyramides de Gizeh", "annee": -2560},
        ]
        self.assertEqual(filtrer_avant_jc(self.DATA), attendu)

    def test_trier_par_annee(self):
        """Doit réordonner chronologiquement (les plus anciennes d'abord)."""
        attendu = [
            {"nom": "Construction des Pyramides de Gizeh", "annee": -2560},
            {"nom": "Fondation de Rome", "annee": -753},
            {"nom": "Chute de Rome", "annee": 476},
            {"nom": "Bataille de Marignan", "annee": 1515},
            {"nom": "Premier pas sur la Lune", "annee": 1969},
        ]
        self.assertEqual(trier_par_annee(self.DATA), attendu)


if __name__ == "__main__":
    unittest.main(verbosity=2)
