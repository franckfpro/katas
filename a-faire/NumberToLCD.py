"""
================================================================================
KATA NUMBER TO LCD - TRADUCTION ET ADAPTATION PYTHON
================================================================================

CONSIGNES :

Objectif : Écrire un programme qui affiche des nombres avec un style d'écran LCD.

Partie 1
--------
Écrivez un programme qui, étant donné un nombre (avec un nombre arbitraire 
de chiffres), le convertit en nombres de style LCD en utilisant le format 
standard suivant (chaque chiffre fait 3 lignes de haut et utilise des 
caractères '_' et '|') :

    _  _     _  _  _  _  _  _ 
  | _| _||_||_ |_   ||_||_||_|
  ||_  _|  | _||_|  ||_| _|  |

Note : Veuillez NE PAS lire la deuxième partie avant d'avoir terminé la première. 
Une partie du but de ce kata est de vous faire pratiquer la refactorisation et 
l'adaptation aux changements de spécifications.

Partie 2
--------
Modifiez votre programme pour supporter une largeur (width) et une hauteur 
(height) variables pour les chiffres.
Par exemple, pour width = 3 et height = 2, le chiffre 2 s'affichera ainsi :

  ___ 
     |
     |
  ___|
 |
 |
 |___ 

================================================================================
"""

import unittest

# ==============================================================================
# LOGIQUE MÉTIER
# ==============================================================================

# Modélisation d'un afficheur 7 segments pour chaque chiffre (0-9).
# Chaque tuple représente l'état d'activation (True/False) des segments dans 
# l'ordre suivant : (Haut, Haut-Gauche, Haut-Droit, Milieu, Bas-Gauche, Bas-Droit, Bas)
LCD_MAPPING = {
    '0': (True,  True,  True,  False, True,  True,  True),
    '1': (False, False, True,  False, False, True,  False),
    '2': (True,  False, True,  True,  True,  False, True),
    '3': (True,  False, True,  True,  False, True,  True),
    '4': (False, True,  True,  True,  False, True,  False),
    '5': (True,  True,  False, True,  False, True,  True),
    '6': (True,  True,  False, True,  True,  True,  True),
    '7': (True,  False, True,  False, False, True,  False),
    '8': (True,  True,  True,  True,  True,  True,  True),
    '9': (True,  True,  True,  True,  False, True,  True)
}

def number_to_lcd(number: int, width: int = 1, height: int = 1) -> str:
    """
    Convertit un nombre en son équivalent ASCII-art LCD.
    
    :param number: Le nombre entier à convertir.
    :param width: La largeur des segments horizontaux (défaut = 1).
    :param height: La hauteur des segments verticaux (défaut = 1).
    :return: Une chaîne de caractères représentant l'affichage LCD.
    """
    num_str = str(number)
    
    # La hauteur totale d'un chiffre est de (2 * height) + 1 lignes
    total_lines = 2 * height + 1
    lines = [[] for _ in range(total_lines)]

    for digit in num_str:
        top, tl, tr, mid, bl, br, bot = LCD_MAPPING[digit]

        # Ligne 0 : Segment du Haut
        lines[0].append(' ' + ('_' if top else ' ') * width + ' ')

        # Lignes 1 à height-1 : Segments Verticaux Supérieurs (sans le milieu)
        for i in range(1, height):
            lines[i].append(('|' if tl else ' ') + ' ' * width + ('|' if tr else ' '))

        # Ligne height : Fin des Segments Verticaux Supérieurs + Segment du Milieu
        lines[height].append(('|' if tl else ' ') + ('_' if mid else ' ') * width + ('|' if tr else ' '))

        # Lignes height+1 à 2*height-1 : Segments Verticaux Inférieurs (sans le bas)
        for i in range(height + 1, 2 * height):
            lines[i].append(('|' if bl else ' ') + ' ' * width + ('|' if br else ' '))

        # Ligne 2*height : Fin des Segments Verticaux Inférieurs + Segment du Bas
        lines[2 * height].append(('|' if bl else ' ') + ('_' if bot else ' ') * width + ('|' if br else ' '))

    # Concaténation finale avec un espace d'espacement entre chaque chiffre
    return '\n'.join(' '.join(row) for row in lines)


# ==============================================================================
# TESTS UNITAIRES
# ==============================================================================

class TestNumberToLCD(unittest.TestCase):

    def test_part_1_single_digit(self):
        """Valide le format de base (taille 1x1) pour un chiffre simple."""
        expected_2 = (
            " _ \n"
            " _|\n"
            "|_ "
        )
        self.assertEqual(number_to_lcd(2), expected_2)

    def test_part_1_multiple_digits(self):
        """Valide le format de base pour plusieurs chiffres (ex: 0123456789)."""
        expected_10 = (
            "    _ \n"
            "  || |\n"
            "  ||_|"
        )
        self.assertEqual(number_to_lcd(10), expected_10)

    def test_part_2_variable_width(self):
        """Valide que la largeur (width) peut être modifiée sans toucher la hauteur."""
        expected = (
            " ___ \n"
            " ___|\n"
            "|___ "
        )
        self.assertEqual(number_to_lcd(2, width=3, height=1), expected)

    def test_part_2_variable_height(self):
        """Valide que la hauteur (height) peut être modifiée sans toucher la largeur."""
        expected = (
            " _ \n"
            "  |\n"
            " _|\n"
            "|  \n"
            "|_ "
        )
        self.assertEqual(number_to_lcd(2, width=1, height=2), expected)

    def test_part_2_variable_width_and_height(self):
        """Valide l'exemple exact de la Partie 2 (width=3, height=2) pour le chiffre 2."""
        expected = (
            " ___ \n"
            "    |\n"
            " ___|\n"
            "|    \n"
            "|___ "
        )
        self.assertEqual(number_to_lcd(2, width=3, height=2), expected)

    def test_part_2_complex_number(self):
        """Valide un nombre complexe avec des dimensions élargies."""
        # Test avec "80" (width=2, height=2)
        expected = (
            " __   __ \n"
            "|  | |  |\n"
            "|__| |  |\n"
            "|  | |  |\n"
            "|__| |__|"
        )
        self.assertEqual(number_to_lcd(80, width=2, height=2), expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)