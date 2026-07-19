import unittest

# =============================================================================
# KATA : TIC TAC TOE (MORPION)
# =============================================================================
#
# CONSIGNES :
# Les règles du jeu de Tic Tac Toe sont les suivantes :
# - Il y a deux joueurs dans le jeu (X et O).
# - Les joueurs jouent à tour de rôle en prenant des cases jusqu'à ce que le jeu soit terminé.
# - Un joueur peut prendre une case si elle n'est pas déjà prise.
# - Un jeu est terminé quand toutes les cases d'une ligne sont prises par un joueur.
# - Un jeu est terminé quand toutes les cases d'une colonne sont prises par un joueur.
# - Un jeu est terminé quand toutes les cases d'une diagonale sont prises par un joueur.
# - Un jeu est terminé quand toutes les cases sont prises (match nul).
# =============================================================================

class TicTacToe:
    def __init__(self):
        """Initialise un nouveau jeu de Tic Tac Toe avec une grille vide."""
        # Grille de 3x3 initialisée avec des chaînes vides
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # X commence toujours
        self.winner = None
        self.is_over = False

    def play(self, row: int, col: int):
        """Permet au joueur courant de jouer sur la case (row, col)."""
        if self.is_over:
            raise ValueError("Le jeu est déjà terminé.")
            
        if not (0 <= row <= 2 and 0 <= col <= 2):
            raise IndexError("Les coordonnées doivent être comprises entre 0 et 2.")
            
        if self.board[row][col] != '':
            raise ValueError("Cette case est déjà prise.")

        # Le joueur prend la case
        self.board[row][col] = self.current_player
        
        # Vérification de l'état du jeu après le coup
        self._check_game_over()

        # Changement de joueur si le jeu n'est pas terminé
        if not self.is_over:
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def _check_game_over(self):
        """Vérifie si le jeu est terminé par une victoire ou un match nul."""
        # Vérification des lignes et des colonnes
        for i in range(3):
            # Lignes
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                self.winner = self.board[i][0]
                self.is_over = True
                return
            # Colonnes
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                self.winner = self.board[0][i]
                self.is_over = True
                return

        # Vérification des diagonales
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            self.winner = self.board[0][0]
            self.is_over = True
            return
            
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            self.winner = self.board[0][2]
            self.is_over = True
            return

        # Vérification du match nul (toutes les cases sont prises)
        is_full = all(self.board[r][c] != '' for r in range(3) for c in range(3))
        if is_full:
            self.is_over = True


# =============================================================================
# TESTS UNITAIRES
# =============================================================================

class TestTicTacToe(unittest.TestCase):

    def setUp(self):
        """Initialise une nouvelle partie avant chaque test."""
        self.game = TicTacToe()

    def test_initial_state(self):
        """Le jeu doit commencer avec le joueur X et ne pas être terminé."""
        self.assertEqual(self.game.current_player, 'X')
        self.assertFalse(self.game.is_over)
        self.assertIsNone(self.game.winner)

    def test_alternate_turns(self):
        """Les joueurs doivent jouer à tour de rôle."""
        self.game.play(0, 0) # X joue
        self.assertEqual(self.game.current_player, 'O')
        self.game.play(0, 1) # O joue
        self.assertEqual(self.game.current_player, 'X')

    def test_field_already_taken(self):
        """Un joueur ne peut pas prendre une case déjà prise."""
        self.game.play(1, 1)
        with self.assertRaises(ValueError):
            self.game.play(1, 1) # Le joueur suivant tente de prendre la même case

    def test_win_by_row(self):
        """Le jeu est terminé quand toutes les cases d'une ligne sont prises par un joueur."""
        self.game.play(0, 0) # X
        self.game.play(1, 0) # O
        self.game.play(0, 1) # X
        self.game.play(1, 1) # O
        self.game.play(0, 2) # X gagne sur la première ligne
        
        self.assertTrue(self.game.is_over)
        self.assertEqual(self.game.winner, 'X')

    def test_win_by_column(self):
        """Le jeu est terminé quand toutes les cases d'une colonne sont prises par un joueur."""
        self.game.play(0, 1) # X
        self.game.play(0, 0) # O
        self.game.play(1, 1) # X
        self.game.play(1, 0) # O
        self.game.play(2, 2) # X
        self.game.play(2, 0) # O gagne sur la première colonne
        
        self.assertTrue(self.game.is_over)
        self.assertEqual(self.game.winner, 'O')

    def test_win_by_diagonal(self):
        """Le jeu est terminé quand toutes les cases d'une diagonale sont prises par un joueur."""
        self.game.play(0, 0) # X
        self.game.play(0, 1) # O
        self.game.play(1, 1) # X
        self.game.play(0, 2) # O
        self.game.play(2, 2) # X gagne sur la diagonale principale
        
        self.assertTrue(self.game.is_over)
        self.assertEqual(self.game.winner, 'X')

    def test_draw_all_fields_taken(self):
        """Le jeu est terminé quand toutes les cases sont prises (Match Nul)."""
        moves = [
            (0, 0), (0, 1), (0, 2),
            (1, 1), (1, 0), (1, 2),
            (2, 1), (2, 0), (2, 2)
        ]
        # Déroulement menant à un match nul
        for r, c in moves:
            self.game.play(r, c)
            
        self.assertTrue(self.game.is_over)
        self.assertIsNone(self.game.winner)

    def test_cannot_play_if_game_is_over(self):
        """Un joueur ne peut pas jouer si la partie est déjà terminée."""
        self.test_win_by_row() # X gagne
        with self.assertRaises(ValueError):
            self.game.play(2, 2)

if __name__ == '__main__':
    unittest.main()