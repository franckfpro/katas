"""
KATA PYTHON #045 - Le Compresseur RLE (Run-Length Encoding)
Difficulté : 5/10

ÉNONCÉ :
La compression RLE (Run-Length Encoding) est une méthode simple de compression
de données où les vagues de caractères identiques consécutifs sont remplacées
pas le caractère suivi du nombre de fois qu'il apparaît.

On vous demande de compléter la fonction `compresser_rle`.

RÈGLES ET CONTRAINTES :
1. La fonction prend une chaîne de caractères `texte` et renvoie sa version compressée.
2. Si le texte est vide, renvoyez une chaîne vide.
3. Attention : Même si un caractère n'apparaît qu'une seule fois, il doit TOUTEFOIS
   être suivi du chiffre 1 (ex: "A" devient "A1").
4. Le comportement doit être sensible à la casse ("A" et "a" sont deux groupes distincts).

Exemples :
- "AAAABBBCC" -> "A4B3C2"
- "ABC" -> "A1B1C1"
- "aAABBBb" -> "a1A2B3b1"
"""

import unittest


def compresser_rle(texte: str) -> str:
    """Compresse une chaîne de caractères en utilisant l'algorithme RLE."""
    if len(texte) == 0:
        return ""
    result = []
    resultstring = ""
    result.append(texte[0])
    result.append(1)
    for letter in texte[1:]:
        if letter == result[-2]:
            result[-1] += 1
        else:
            result.append(letter)
            result.append(1)
    for e in result:
        resultstring += str(e)

    return resultstring


# =====================================================================
# TESTS UNITAIRES (Ne pas modifier cette section)
# =====================================================================


class TestCompressionRLE(unittest.TestCase):
    """Suite de tests pour valider votre fonction compresser_rle."""

    def test_chaine_vide(self):
        """Une chaîne vide doit retourner une chaîne vide."""
        self.assertEqual(compresser_rle(""), "")

    def test_caracteres_uniques_repetes(self):
        """Cas standard avec des blocs de répétitions nets."""
        self.assertEqual(compresser_rle("AAAAABBBCC"), "A5B3C2")

    def test_sans_repetition(self):
        """Chaque caractère doit avoir son compteur à 1."""
        self.assertEqual(compresser_rle("XYZ"), "X1Y1Z1")

    def test_sensibilite_casse(self):
        """Les majuscules et minuscules ne doivent pas se mélanger."""
        self.assertEqual(compresser_rle("AAaaB"), "A2a2B1")

    def test_alternance_complexes(self):
        """Vérifie que le retour d'un même caractère plus loin crée un nouveau bloc."""
        # Le second bloc de 'A' doit être compté séparément
        self.assertEqual(compresser_rle("AABBAA"), "A2B2A2")

    def test_avec_espaces(self):
        """Les espaces sont des caractères comme les autres et doivent être compressés."""
        self.assertEqual(compresser_rle("   A "), " 3A1 1")


if __name__ == "__main__":
    unittest.main(verbosity=2)
