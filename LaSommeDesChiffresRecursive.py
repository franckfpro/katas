"""
KATA PYTHON #048 - La Somme des Chiffres Récursive
Difficulté : 3/10

ÉNONCÉ :
On vous demande d'écrire une fonction RECURSIVE `somme_chiffres` qui prend un
nombre entier positif ou nul `n` en paramètre et retourne la somme de tous ses
chiffres.

INTERDICTION :
Il est strictement interdit d'utiliser des boucles (`for`, `while`) ou de
convertir le nombre en chaîne de caractères (`str(n)`). Vous devez utiliser
uniquement des opérations mathématiques et la récursion.

RÈGLES ET CONTRAINTES :
1. Si le nombre ne contient qu'un seul chiffre (de 0 à 9), la somme est le nombre lui-même.
2. Pour les nombres plus grands, vous devez extraire le dernier chiffre et faire
   un appel récursif avec le reste du nombre.

Exemples :
- 5 -> 5
- 123 -> 1 + 2 + 3 = 6
- 4002 -> 4 + 0 + 0 + 2 = 6
"""

import unittest


def somme_chiffres(n: int) -> int:
    """Calcule la somme des chiffres d'un entier de manière récursive.

    Interdiction d'utiliser des boucles ou des chaînes de caractères.
    """
    if n <= 9:
        return n
    last = n % 10
    suivant = n // 10
    return last + somme_chiffres(suivant)


# =====================================================================
# TESTS UNITAIRES (Ne pas modifier cette section)
# =====================================================================


class TestSommeChiffresRecursif(unittest.TestCase):
    """Suite de tests pour valider votre fonction récursive somme_chiffres."""

    def test_cas_de_base(self):
        """Un seul chiffre doit retourner le chiffre lui-même."""
        self.assertEqual(somme_chiffres(0), 0)
        self.assertEqual(somme_chiffres(5), 5)
        self.assertEqual(somme_chiffres(9), 9)

    def test_nombres_standard(self):
        """Vérifie la somme pour des nombres à plusieurs chiffres."""
        self.assertEqual(somme_chiffres(12), 3)  # 1 + 2
        self.assertEqual(somme_chiffres(123), 6)  # 1 + 2 + 3
        self.assertEqual(somme_chiffres(9875), 29)  # 9 + 8 + 7 + 5

    def test_avec_des_zeros(self):
        """Les zéros ne doivent pas perturber le calcul récursif."""
        self.assertEqual(somme_chiffres(1002), 3)  # 1 + 0 + 0 + 2
        self.assertEqual(somme_chiffres(50), 5)

    def test_grand_nombre(self):
        """Vérifie que la récursion s'empile correctement sur un grand nombre."""
        self.assertEqual(somme_chiffres(1111111111), 10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
