"""
KATA PYTHON #043 - Le Détecteur d'Isogrammes
Difficulté : 3/10

ÉNONCÉ :
Un isogramme est un mot (ou une phrase) qui ne contient aucune lettre répétée.
En d'autres termes, chaque lettre doit y apparaître exactement une seule fois.

On vous demande de compléter la fonction `est_isogramme` qui prend en paramètre
une chaîne de caractères `texte` et renvoie un booléen (`True` ou `False`).

RÈGLES ET CONTRAINTES :
1. La casse doit être ignorée : "A" et "a" sont considérés comme la même lettre.
2. Les espaces et les tirets ("-") ne comptent PAS comme des répétitions. Ils 
   peuvent apparaître plusieurs fois sans invalider l'isogramme.
3. Si la chaîne est vide, elle est considérée comme un isogramme valide.

Exemples :
- "Dermatoglyphics" -> True (toutes les lettres sont uniques)
- "baba" -> False (le 'b' et le 'a' se répètent)
- "arrière-grand-père" -> False (les tirets et espaces sont légaux, mais le 'r' se répète)
- "six-year-old" -> True (les tirets sont légaux, aucune lettre ne se répète)
"""

import unittest


def est_isogramme(texte: str) -> bool:
    """Vérifie si une chaîne de caractères est un isogramme.

    Un isogramme est un mot où aucune lettre n'est répétée.
    Les espaces et les tirets sont ignorés.
    """
    count = {}
    for letter in texte:
        if letter != " " and letter != "-":
            if letter not in count:
                count[letter] = 1
            else:
                count[letter] += 1
    for val in count.values():
        if val > 1:
            return False
    return True


# =====================================================================
# TESTS UNITAIRES (Ne pas modifier cette section)
# =====================================================================

class TestIsogramme(unittest.TestCase):
    """Suite de tests pour valider votre fonction est_isogramme."""

    def test_isogrammes_valides(self):
        """Vérifie les mots qui sont de vrais isogrammes."""
        self.assertTrue(est_isogramme(""))
        self.assertTrue(est_isogramme("dermatoglyphics"))
        self.assertTrue(est_isogramme("subdermatoglyphic"))
        self.assertTrue(est_isogramme("unclopyrightabe"))

    def test_isogrammes_avec_majuscules(self):
        """La casse ne devrait pas impacter le résultat."""
        self.assertTrue(est_isogramme("Alphabet"))  # 'A' et 'a' se répètent
        self.assertFalse(est_isogramme("Abba"))      # Répétitions multiples

    def test_mots_invalides(self):
        """Vérifie les mots qui ont des lettres répétées."""
        self.assertFalse(est_isogramme("aba"))
        self.assertFalse(est_isogramme("moose"))
        self.assertTrue(est_isogramme("déjà-vu"))

    def test_caracteres_speciaux_autorises(self):
        """Les espaces et tirets ne doivent pas invalider le mot."""
        self.assertTrue(est_isogramme("six-year-old"))
        self.assertTrue(est_isogramme("thumbscrew-jingly"))
        self.assertFalse(est_isogramme("arrière-grand-père"))  # 'r', 'e', etc. se répètent


if __name__ == "__main__":
    # Exécute les tests. Ils échoueront tant que la fonction n'est pas codée.
    unittest.main(verbosity=2)
