"""
Kata Mastermind - Consignes

Avez-vous déjà joué au Mastermind ? C'est un jeu où un joueur (le créateur du code) 
choisit une combinaison secrète de pions de couleur, et un autre joueur (le décodeur) 
doit la deviner. À chaque tentative du décodeur, le créateur du code répond en 
indiquant uniquement le nombre de couleurs bien placées et le nombre de couleurs 
correctes mais mal placées.

Objectif :
L'idée de ce Kata est de coder un algorithme capable de jouer le rôle de l'évaluateur.
Votre fonction doit retourner, pour une combinaison secrète et une tentative données :
- Le nombre de couleurs bien placées (exact matches).
- Le nombre de couleurs correctes mais mal placées (misplaced).

Règles :
- Une combinaison peut contenir n'importe quel nombre de pions, mais le secret et la 
  tentative auront la même longueur.
- Vous pouvez utiliser n'importe quel nombre de couleurs.
- Attention à ne pas compter une couleur mal placée si elle a déjà été associée à un 
  autre pion (gestion des doublons).

Exemple :
Pour un secret ['bleu', 'rouge', 'vert', 'rose'] et une tentative ['jaune', 'rouge', 'bleu', 'violet'],
la réponse doit être : 1 bien placé (rouge) et 1 mal placé (bleu).
"""

import unittest
from collections import Counter

def evaluate_guess(secret, guess):
    """
    Évalue une tentative au Mastermind par rapport à une combinaison secrète.
    
    Args:
        secret (list): La combinaison secrète de couleurs.
        guess (list): La tentative du joueur.
        
    Returns:
        tuple: (nombre de couleurs bien placées, nombre de couleurs mal placées)
    """
    well_placed = 0
    
    # Listes pour stocker les couleurs qui ne sont pas "bien placées"
    remaining_secret = []
    remaining_guess = []

    # 1er passage : on compte les "bien placés" et on met de côté le reste
    for s_color, g_color in zip(secret, guess):
        if s_color == g_color:
            well_placed += 1
        else:
            remaining_secret.append(s_color)
            remaining_guess.append(g_color)

    # 2ème passage : on compte les "mal placés" à l'aide des occurrences restantes
    misplaced = 0
    secret_counts = Counter(remaining_secret)
    guess_counts = Counter(remaining_guess)

    for color, count in guess_counts.items():
        if color in secret_counts:
            # On ajoute le minimum entre l'occurrence dans la tentative et dans le secret
            # pour ne pas compter une couleur plus de fois qu'elle n'est disponible.
            misplaced += min(count, secret_counts[color])

    return well_placed, misplaced


# ==========================================
# SUITE DE TESTS UNITAIRES
# ==========================================

class TestMastermind(unittest.TestCase):
    
    def test_example_from_instructions(self):
        # Le cas d'usage fourni dans les consignes
        secret = ['bleu', 'rouge', 'vert', 'rose']
        guess = ['jaune', 'rouge', 'bleu', 'violet']
        self.assertEqual(evaluate_guess(secret, guess), (1, 1))

    def test_all_well_placed(self):
        # Victoire parfaite
        secret = ['rouge', 'bleu', 'vert']
        guess = ['rouge', 'bleu', 'vert']
        self.assertEqual(evaluate_guess(secret, guess), (3, 0))

    def test_completely_wrong(self):
        # Aucune couleur en commun
        secret = ['rouge', 'bleu', 'vert']
        guess = ['jaune', 'rose', 'violet']
        self.assertEqual(evaluate_guess(secret, guess), (0, 0))

    def test_all_misplaced(self):
        # Les bonnes couleurs mais au mauvais endroit
        secret = ['rouge', 'bleu', 'vert']
        guess = ['bleu', 'vert', 'rouge']
        self.assertEqual(evaluate_guess(secret, guess), (0, 3))

    def test_duplicates_in_guess(self):
        # La tentative contient plus de 'rouge' qu'il n'y en a dans le secret
        secret = ['rouge', 'bleu', 'vert']
        guess = ['rouge', 'rouge', 'rouge']
        self.assertEqual(evaluate_guess(secret, guess), (1, 0))

    def test_duplicates_in_secret_and_guess(self):
        # Test complexe avec des doublons des deux côtés
        secret = ['rouge', 'rouge', 'bleu', 'jaune']
        guess = ['bleu', 'rouge', 'rouge', 'rouge']
        # Secret restant : ['rouge', 'bleu', 'jaune']
        # Guess restant  : ['bleu', 'rouge', 'rouge']
        # Bien placés : 1 (le 2ème rouge)
        # Mal placés : 1 'bleu' + 1 'rouge' = 2
        self.assertEqual(evaluate_guess(secret, guess), (1, 2))


if __name__ == '__main__':
    unittest.main()