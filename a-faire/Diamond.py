"""
Kata Diamond - Consignes

Étant donné une lettre de l'alphabet, affichez un diamant commençant par 'A', 
avec la lettre fournie au point le plus large.

Règles :
- La première ligne contient une seule lettre 'A'.
- La dernière ligne contient une seule lettre 'A'.
- Toutes les lignes, sauf la première et la dernière, comportent exactement deux lettres.
- Le diamant est symétrique horizontalement et verticalement.
- Le diamant a une forme carrée (le nombre de lignes est égal au nombre de colonnes).
- La ligne la plus large contient la lettre cible.
- L'espace extérieur aux lettres diminue à mesure que l'on s'approche de la lettre cible, 
  et augmente à mesure que l'on s'en éloigne.
- L'espace intérieur aux lettres augmente à mesure que l'on s'approche de la lettre cible, 
  et diminue à mesure que l'on s'en éloigne.

Exemple d'affichage pour la lettre 'C' :
  A  
 B B 
C   C
 B B 
  A  
"""

import unittest

def generate_diamond(letter: str) -> str:
    """
    Génère un motif en forme de diamant en fonction de la lettre cible.
    
    Args:
        letter (str): La lettre cible (le point le plus large du diamant).
        
    Returns:
        str: Le diamant sous forme de chaîne de caractères.
    """
    letter = letter.upper()
    
    # Distance de la lettre cible par rapport à 'A' (ex: A=0, B=1, C=2)
    n = ord(letter) - ord('A')
    
    lines = []
    
    # Étape 1 : Construire la moitié supérieure (incluant la ligne du milieu)
    for i in range(n + 1):
        current_char = chr(ord('A') + i)
        outer_spaces = " " * (n - i)
        
        if i == 0:
            # Pour 'A', il n'y a qu'une seule lettre au centre
            lines.append(f"{outer_spaces}{current_char}{outer_spaces}")
        else:
            # Pour les autres lettres, on a des espaces intérieurs
            inner_spaces = " " * (2 * i - 1)
            lines.append(f"{outer_spaces}{current_char}{inner_spaces}{current_char}{outer_spaces}")
            
    # Étape 2 : Construire la moitié inférieure en reflétant la moitié supérieure
    # (On parcourt la liste à l'envers, en omettant la dernière ligne générée qui est le milieu)
    for i in range(n - 1, -1, -1):
        current_char = chr(ord('A') + i)
        outer_spaces = " " * (n - i)
        
        if i == 0:
            lines.append(f"{outer_spaces}{current_char}{outer_spaces}")
        else:
            inner_spaces = " " * (2 * i - 1)
            lines.append(f"{outer_spaces}{current_char}{inner_spaces}{current_char}{outer_spaces}")
            
    # Assembler avec des retours à la ligne
    return "\n".join(lines)


# ==========================================
# SUITE DE TESTS UNITAIRES
# ==========================================

class TestDiamondKata(unittest.TestCase):
    
    def test_diamond_A(self):
        expected = "A"
        self.assertEqual(generate_diamond('A'), expected)
        
    def test_diamond_B(self):
        expected = (
            " A \n"
            "B B\n"
            " A "
        )
        self.assertEqual(generate_diamond('B'), expected)
        
    def test_diamond_C(self):
        expected = (
            "  A  \n"
            " B B \n"
            "C   C\n"
            " B B \n"
            "  A  "
        )
        self.assertEqual(generate_diamond('C'), expected)

    def test_diamond_E(self):
        expected = (
            "    A    \n"
            "   B B   \n"
            "  C   C  \n"
            " D     D \n"
            "E       E\n"
            " D     D \n"
            "  C   C  \n"
            "   B B   \n"
            "    A    "
        )
        self.assertEqual(generate_diamond('E'), expected)

    def test_lower_case_input(self):
        # Le programme devrait gérer les lettres minuscules et les traiter comme des majuscules
        self.assertEqual(generate_diamond('b'), generate_diamond('B'))

if __name__ == '__main__':
    unittest.main()