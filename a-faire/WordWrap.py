"""
======================================================================
KATA : WORD WRAP (Retour à la ligne)
======================================================================

CONSIGNES :
L'objectif est d'écrire une fonction nommée `wrap` qui prend deux arguments : 
une chaîne de caractères (string) et un nombre de colonnes (entier).

La fonction doit retourner la chaîne de caractères modifiée, avec des 
sauts de ligne (`\\n`) insérés aux bons endroits pour s'assurer qu'aucune 
ligne n'est plus longue que le nombre de colonnes autorisé.

Règles de découpe :
- Vous devez essayer de couper les lignes aux limites des mots.
- Comme un traitement de texte, coupez la ligne en remplaçant le dernier 
  espace d'une ligne par un saut de ligne.
- Si un seul mot est plus long que le nombre de colonnes, vous devrez 
  le couper de force à la limite de la colonne.

======================================================================
"""

import unittest

# --- CODE MÉTIER À TESTER ---

def wrap(text: str, column_length: int) -> str:
    """
    Formate une chaîne de caractères pour qu'aucune ligne ne dépasse 
    la longueur spécifiée par `column_length`.
    """
    # Cas de base : chaîne vide ou suffisamment courte
    if not text:
        return ""
    if len(text) <= column_length:
        return text

    # Chercher le dernier espace dans la limite de la colonne
    # On regarde jusqu'à column_length + 1 pour inclure l'espace juste à la limite
    last_space_index = text.rfind(' ', 0, column_length + 1)

    if last_space_index != -1:
        # Un espace a été trouvé, on coupe à cet endroit (en ignorant l'espace)
        return text[:last_space_index] + '\n' + wrap(text[last_space_index + 1:], column_length)
    else:
        # Aucun espace trouvé, on est obligé de couper le mot en plein milieu
        return text[:column_length] + '\n' + wrap(text[column_length:], column_length)


# ======================================================================
# ZONE DE TESTS UNITAIRES
# ======================================================================
class TestWordWrap(unittest.TestCase):

    def test_empty_string_returns_empty(self):
        self.assertEqual(wrap("", 10), "")

    def test_short_string_returns_same_string(self):
        self.assertEqual(wrap("hello", 10), "hello")

    def test_string_exactly_column_length_returns_same(self):
        self.assertEqual(wrap("hello", 5), "hello")

    def test_split_one_word_longer_than_column_length(self):
        # Le mot est coupé de force car il n'y a pas d'espaces
        self.assertEqual(wrap("hello", 3), "hel\nlo")

    def test_split_two_words_on_space(self):
        # La coupure doit se faire sur l'espace
        self.assertEqual(wrap("hello world", 7), "hello\nworld")

    def test_split_three_words_on_spaces(self):
        self.assertEqual(wrap("hello world here", 7), "hello\nworld\nhere")

    def test_split_long_word_mixed_with_spaces(self):
        # "hello" passe, mais "worldhere" est trop long (9 > 7) et doit être coupé
        self.assertEqual(wrap("hello worldhere", 7), "hello\nworldhe\nre")

    def test_space_exactly_at_column_limit(self):
        # L'espace est exactement à l'index 5, il doit être remplacé par le saut de ligne
        self.assertEqual(wrap("hello world", 5), "hello\nworld")


if __name__ == '__main__':
    unittest.main()