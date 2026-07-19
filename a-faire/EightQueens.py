import unittest

# ==============================================================================
# CONSIGNES DU KATA : LES HUIT REINES (EIGHT QUEENS)
# ==============================================================================
# Règles de base :
# Ce kata est basé sur les règles classiques des échecs. Vous devez placer 
# huit reines sur un échiquier 8x8 de manière à ce qu'aucune d'entre elles 
# ne puisse en capturer une autre (aucune reine sur la même ligne, même 
# colonne ou même diagonale).
# Astuce : Il ne peut y avoir qu'une seule reine par ligne et par colonne.
#
# Étape 1 :
# Utilisez des boucles TDD pour construire un programme qui trouve TOUTES 
# les solutions possibles.
# 
# Parcours d'arbre (Tree Traversal) :
# - Écrivez un programme utilisant un parcours en profondeur (Depth-first).
# - Écrivez un programme utilisant un parcours en largeur (Breadth-first).
# - Comparez les performances et la lisibilité.
#
# Bonus (Spoiler Technique) : L'approche bit-à-bit
# Pour optimiser drastiquement la solution "force brute", il est possible 
# d'encoder chaque ligne sur un octet (8 bits). 
# - Lignes/Colonnes : L'opérateur OR permet de vérifier les collisions.
# - Diagonales : Peuvent être vérifiées avec un décalage de bit (shift) par ligne.
# ==============================================================================

class EightQueens:
    def __init__(self, size: int = 8):
        """
        Initialise le solveur pour un échiquier de taille NxN.
        """
        self.size = size

    def is_safe(self, board: list[int], current_row: int, current_col: int) -> bool:
        """
        Vérifie si une reine peut être placée en (current_row, current_col) 
        sans être menacée par les reines déjà placées sur les lignes précédentes.
        
        'board' est une liste où l'index est la ligne et la valeur est la colonne.
        Ex: board = [3, 0] signifie reine en (0,3) et reine en (1,0).
        """
        for r, c in enumerate(board):
            # Vérification de la même colonne
            if c == current_col:
                return False
            # Vérification des diagonales (différence des X == différence des Y)
            if abs(c - current_col) == abs(r - current_row):
                return False
        return True

    def solve_dfs(self) -> list[list[int]]:
        """
        Trouve toutes les solutions en utilisant un parcours en profondeur (DFS / Backtracking).
        Retourne une liste de toutes les configurations valides.
        """
        solutions = []

        def backtrack(row: int, current_board: list[int]):
            # Condition d'arrêt : on a placé une reine sur chaque ligne
            if row == self.size:
                solutions.append(current_board[:])
                return

            # Essayer de placer une reine sur chaque colonne de la ligne courante
            for col in range(self.size):
                if self.is_safe(current_board, row, col):
                    current_board.append(col)       # Placer la reine
                    backtrack(row + 1, current_board) # Explorer la branche
                    current_board.pop()             # Retirer la reine (backtrack)

        backtrack(0, [])
        return solutions


# ==============================================================================
# TESTS UNITAIRES
# ==============================================================================

class TestEightQueens(unittest.TestCase):

    def test_is_safe_valid_placement(self):
        solver = EightQueens(size=4)
        # Échiquier avec une reine en (0, 1)
        board = [1]
        # Placer en (1, 3) devrait être sûr (pas même col, pas même diag)
        self.assertTrue(solver.is_safe(board, 1, 3))

    def test_is_safe_same_column(self):
        solver = EightQueens(size=4)
        board = [1]
        # Placer en (1, 1) provoque une collision de colonne
        self.assertFalse(solver.is_safe(board, 1, 1))

    def test_is_safe_diagonal(self):
        solver = EightQueens(size=4)
        board = [1]
        # Placer en (1, 0) ou (1, 2) provoque une collision diagonale
        self.assertFalse(solver.is_safe(board, 1, 0))
        self.assertFalse(solver.is_safe(board, 1, 2))

    def test_solve_4_queens(self):
        # Pour un plateau 4x4, il existe exactement 2 solutions distinctes
        solver = EightQueens(size=4)
        solutions = solver.solve_dfs()
        self.assertEqual(len(solutions), 2)
        # Vérification des solutions connues pour N=4
        self.assertIn([1, 3, 0, 2], solutions)
        self.assertIn([2, 0, 3, 1], solutions)

    def test_solve_8_queens(self):
        # Pour le problème classique des 8 reines, il existe 92 solutions distinctes
        solver = EightQueens(size=8)
        solutions = solver.solve_dfs()
        self.assertEqual(len(solutions), 92)

    def test_solve_1_queen(self):
        # Pour un plateau 1x1, il y a 1 solution
        solver = EightQueens(size=1)
        solutions = solver.solve_dfs()
        self.assertEqual(len(solutions), 1)
        self.assertEqual(solutions[0], [0])

    def test_solve_2_and_3_queens(self):
        # Pour des plateaux 2x2 et 3x3, il n'y a aucune solution possible
        self.assertEqual(len(EightQueens(size=2).solve_dfs()), 0)
        self.assertEqual(len(EightQueens(size=3).solve_dfs()), 0)


if __name__ == '__main__':
    unittest.main()