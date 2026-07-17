import unittest

# =====================================================================
# CONSIGNES DU KATA : REVERSI (OTHELLO)
# =====================================================================
# Reversi est un jeu de plateau pour deux joueurs.
#
# L'objectif de ce Kata est d'écrire un programme qui prend une 
# position actuelle du plateau de jeu ainsi que l'information de savoir 
# à qui c'est le tour de jouer, et renvoie une liste des mouvements 
# légaux pour ce joueur. 
#
# Un mouvement n'est légal que s'il entraîne le retournement d'au 
# moins un pion de l'adversaire.
#
# Format :
# - Le plateau est une grille de 8x8.
# - Les colonnes sont nommées de A à H et les lignes de 1 à 8.
# - "." indique une case vide.
# - "B" indique un pion noir (Black).
# - "W" indique un pion blanc (White).
# - Les mouvements légaux doivent être retournés sous forme 
#   de coordonnées (ex: ["C5", "D6", "E3", "F4"]).
# =====================================================================

def get_legal_moves(board: list[str], player: str) -> list[str]:
    """
    Parcourt le plateau et retourne la liste des coordonnées des 
    mouvements légaux pour le joueur donné.
    """
    opponent = 'W' if player == 'B' else 'B'
    
    # Vecteurs pour les 8 directions (dy, dx)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]
    
    legal_moves = []

    for r in range(8):
        for c in range(8):
            # On ne peut jouer que sur une case vide
            if board[r][c] != '.':
                continue
                
            is_legal = False
            
            # Vérification des 8 directions autour de la case vide
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                found_opponent = False
                
                # Avancer tant qu'on trouve des pions adverses
                while 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc] == opponent:
                    found_opponent = True
                    nr += dr
                    nc += dc
                
                # Si on a trouvé au moins un pion adverse, et que la case suivante
                # est un pion de notre propre couleur, alors le mouvement est légal.
                if found_opponent and 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc] == player:
                    is_legal = True
                    break # Pas besoin de vérifier d'autres directions pour cette case
            
            if is_legal:
                # Convertir les index (r, c) en format d'échecs (ex: C5)
                col_str = chr(ord('A') + c)
                row_str = str(r + 1)
                legal_moves.append(f"{col_str}{row_str}")

    return sorted(legal_moves)


# =====================================================================
# TESTS UNITAIRES
# =====================================================================
class TestReversi(unittest.TestCase):

    def setUp(self):
        # Configuration initiale classique du plateau
        self.initial_board = [
            "........",
            "........",
            "........",
            "...WB...",
            "...BW...",
            "........",
            "........",
            "........"
        ]

    def test_legal_moves_for_black_initial_state(self):
        # Au début du jeu, les Noirs (B) ont 4 coups possibles.
        expected_moves = ["C4", "D3", "E6", "F5"]
        result = get_legal_moves(self.initial_board, 'B')
        self.assertEqual(result, sorted(expected_moves))

    def test_legal_moves_for_white_initial_state(self):
        # Pareil pour les Blancs (W) au premier tour.
        expected_moves = ["C5", "D6", "E3", "F4"]
        result = get_legal_moves(self.initial_board, 'W')
        self.assertEqual(result, sorted(expected_moves))

    def test_no_legal_moves(self):
        # Si le plateau est rempli d'une seule couleur, aucun mouvement légal
        board = [
            "BBBBBBBB",
            "BBBBBBBB",
            "BBBBBBBB",
            "BBBBBBBB",
            "BBBBBBBB",
            "BBBBBBBB",
            "BBBBBBBB",
            "BBBBBBBB"
        ]
        self.assertEqual(get_legal_moves(board, 'B'), [])
        self.assertEqual(get_legal_moves(board, 'W'), [])

    def test_complex_scenario(self):
        # Un scénario plus complexe où un coup retourne plusieurs pions 
        # dans différentes directions.
        board = [
            "........",
            "........",
            "..W.....",
            "..WB....",
            "..WWB...",
            "..W.W...",
            "........",
            "........"
        ]
        # B peut jouer en D6 (ligne 6, colonne D) pour flipper les W sur la ligne et diagonale.
        # B peut aussi jouer en B2, B3, B4, B5, etc. dépendamment de la configuration.
        moves_b = get_legal_moves(board, 'B')
        self.assertIn("D6", moves_b)
        self.assertIn("B2", moves_b)


if __name__ == '__main__':
    unittest.main()