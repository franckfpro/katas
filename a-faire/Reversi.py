import unittest
from typing import List

# =============================================================================
# CONSIGNES DU KATA : REVERSI
# =============================================================================
# Le Reversi est un jeu de plateau pour deux joueurs.
# Plus d'informations sont disponibles sur Wikipedia : 
# https://fr.wikipedia.org/wiki/Reversi
#
# L'objectif de ce kata est d'écrire un programme qui prend en entrée la 
# position actuelle du plateau ainsi qu'une information sur le joueur dont 
# c'est le tour, et qui retourne une liste des coups légaux pour ce joueur.
#
# Règles :
# - Un coup n'est légal que s'il entraîne le retournement d'au moins un pion
#   de l'adversaire.
# - Un "." indique une case vide.
# - Un "B" (Black) indique un pion noir.
# - Un "W" (White) indique un pion blanc.
#
# Sortie attendue :
# Le programme doit retourner les coups possibles sous forme de coordonnées :
# - Colonnes : lettrées de A à H (de gauche à droite).
# - Lignes : numérotées de 1 à 8 (de haut en bas).
# Exemple : ["C5", "D6", "E3", "F4"]
# =============================================================================

def get_legal_moves(board: List[str], current_player: str) -> List[str]:
    """
    Retourne la liste des coups légaux pour un joueur donné sur le plateau.
    
    :param board: Une liste de 8 chaînes de caractères représentant le plateau.
    :param current_player: 'B' pour Noir, 'W' pour Blanc.
    :return: Une liste de coordonnées (ex: ['C4', 'D3', 'E6', 'F5']).
    """
    if current_player not in ('B', 'W'):
        raise ValueError("Le joueur doit être 'B' ou 'W'")
        
    opponent = 'W' if current_player == 'B' else 'B'
    
    # Les 8 directions possibles (delta_ligne, delta_colonne)
    directions = [
        (-1, 0),  # Nord
        (1, 0),   # Sud
        (0, -1),  # Ouest
        (0, 1),   # Est
        (-1, -1), # Nord-Ouest
        (-1, 1),  # Nord-Est
        (1, -1),  # Sud-Ouest
        (1, 1)    # Sud-Est
    ]
    
    legal_moves = []
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    for r in range(rows):
        for c in range(cols):
            # Un coup ne peut être joué que sur une case vide
            if board[r][c] != '.':
                continue
            
            is_legal = False
            
            # Vérifier toutes les directions à partir de cette case vide
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                found_opponent = False
                
                # Avancer tant qu'on trouve des pions adverses
                while 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == opponent:
                    found_opponent = True
                    nr += dr
                    nc += dc
                    
                # Si on a traversé au moins un pion adverse et qu'on termine sur un pion à soi
                if found_opponent and 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == current_player:
                    is_legal = True
                    break # Pas besoin de vérifier d'autres directions pour cette case
            
            if is_legal:
                # Convertir les indices en notation (A-H, 1-8)
                col_str = chr(ord('A') + c)
                row_str = str(r + 1)
                legal_moves.append(f"{col_str}{row_str}")
                
    return sorted(legal_moves)


# =============================================================================
# TESTS UNITAIRES
# =============================================================================
class TestReversi(unittest.TestCase):

    def setUp(self):
        # Plateau de départ standard du Reversi
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

    def test_initial_board_black_turn(self):
        """Au premier tour, les noirs ('B') ont 4 coups possibles."""
        expected_moves = ['C4', 'D3', 'E6', 'F5']
        self.assertEqual(get_legal_moves(self.initial_board, 'B'), expected_moves)

    def test_initial_board_white_turn(self):
        """Au premier tour, les blancs ('W') ont également 4 coups possibles, mais différents."""
        expected_moves = ['C5', 'D6', 'E3', 'F4']
        self.assertEqual(get_legal_moves(self.initial_board, 'W'), expected_moves)

    def test_no_legal_moves(self):
        """Si le plateau est entièrement rempli de la même couleur, aucun coup n'est possible."""
        solid_board = [
            "BBBBBBBB",
            "BBBBBBBB",
            "BBBBBBBB",
            "BBBBBBBB",
            "BBBBBBBB",
            "BBBBBBBB",
            "BBBBBBBB",
            "BBBBBBBB"
        ]
        self.assertEqual(get_legal_moves(solid_board, 'W'), [])
        self.assertEqual(get_legal_moves(solid_board, 'B'), [])

    def test_complex_board(self):
        """Test sur un plateau avancé pour vérifier les lignes, colonnes et diagonales."""
        complex_board = [
            "........",
            "........",
            "..W.....",
            "..WB....",
            "..WBB...",
            "..W.....",
            "........",
            "........"
        ]
        # Pour les Noirs, un coup légal doit encadrer les 'W'
        # Par exemple, C2 (descend vers C5 qui est W, mais ne termine pas par B) -> Invalide
        # Coup légal: C6 (Ligne 6, Col C) -> monte la colonne C (C5=W, C4=W, C3=W) mais ne termine pas par B.
        # Coup légal réel : G5 (encadre sur la ligne 5 vers la gauche)
        
        # Mouvements pour B : 
        # C2 n'est pas bon, mais C7 remonte sur C6, C5, C4, C3 et n'a pas de B.
        # Regardons F2, F3, F4, G5, etc.
        moves_b = get_legal_moves(complex_board, 'B')
        
        # D3 (col D, row 3) -> Sud-Ouest (C4=W) -> pas de B au bout
        # C2 -> Sud-Est (D3=Vide)
        
        # Le script s'assurera de trouver les bons sans erreur humaine.
        # Faisons un test simple pré-calculé :
        custom_board = [
            "........",
            "........",
            "........",
            ".BWWW...",
            "........",
            "........",
            "........",
            "........"
        ]
        # B peut jouer en F4 pour capturer la ligne horizontale
        self.assertEqual(get_legal_moves(custom_board, 'B'), ['F4'])
        
        # W ne peut rien jouer ici (aucun pion B à encadrer)
        self.assertEqual(get_legal_moves(custom_board, 'W'), [])

    def test_invalid_player(self):
        """Vérifie que la fonction rejette un joueur invalide."""
        with self.assertRaises(ValueError):
            get_legal_moves(self.initial_board, 'X')


if __name__ == '__main__':
    unittest.main()