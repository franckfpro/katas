"""
KATA TENNIS - CONSIGNES

L'objectif de ce kata est d'implémenter le système de score d'un jeu de tennis
opposant deux joueurs.

Règles du jeu :
1. Durant un jeu, chaque joueur commence avec un score de 0. Avec chaque 
   succès, il gagne des points dans cette séquence : 
   0 ("Love"), 15, 30, 40.
2. Si un joueur a 40 et gagne le point suivant, il remporte le jeu, à 
   condition que l'autre joueur n'ait pas également 40.
3. Si les deux joueurs atteignent 40 points (soit 3 points chacun), le 
   score est "Deuce" (Égalité).
4. Lors d'une égalité, le joueur qui marque le point suivant obtient 
   l'"Advantage" (Avantage).
5. Pour remporter le jeu, un joueur ayant l'avantage doit marquer un autre point.
6. Si c'est le joueur n'ayant pas l'avantage qui marque, le score revient 
   à "Deuce" (Égalité), et ainsi de suite.
7. Le score actuel de n'importe quel joueur doit être disponible à tout 
   moment pendant le jeu.

Objectif : Implémenter la classe TennisGame avec les méthodes pour 
enregistrer les points et récupérer le score formaté.
"""

import unittest

class TennisGame:
    def __init__(self, player1_name: str, player2_name: str):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.p1_points = 0
        self.p2_points = 0

    def won_point(self, player_name: str):
        """Enregistre un point gagné par le joueur spécifié."""
        if player_name == self.player1_name:
            self.p1_points += 1
        elif player_name == self.player2_name:
            self.p2_points += 1
        else:
            raise ValueError(f"Joueur inconnu: {player_name}")

    def get_score(self) -> str:
        """Calcule et retourne le score actuel du jeu au format texte."""
        # Cas 1 : Les joueurs sont à égalité
        if self.p1_points == self.p2_points:
            if self.p1_points == 0:
                return "Love-All"
            elif self.p1_points == 1:
                return "15-All"
            elif self.p1_points == 2:
                return "30-All"
            else:
                return "Deuce"
        
        # Cas 2 : Fin de jeu (Au moins un joueur a atteint 4 points ou plus)
        elif self.p1_points >= 4 or self.p2_points >= 4:
            score_diff = self.p1_points - self.p2_points
            if score_diff == 1:
                return f"Advantage {self.player1_name}"
            elif score_diff == -1:
                return f"Advantage {self.player2_name}"
            elif score_diff >= 2:
                return f"Win for {self.player1_name}"
            else:
                return f"Win for {self.player2_name}"
        
        # Cas 3 : Score standard en cours de jeu
        else:
            score_names = ["Love", "15", "30", "40"]
            return f"{score_names[self.p1_points]}-{score_names[self.p2_points]}"


class TestTennisGame(unittest.TestCase):
    def setUp(self):
        self.game = TennisGame("Player 1", "Player 2")

    def play_points(self, p1_points: int, p2_points: int):
        """Fonction utilitaire pour simuler l'attribution de multiples points."""
        for _ in range(p1_points):
            self.game.won_point("Player 1")
        for _ in range(p2_points):
            self.game.won_point("Player 2")

    def test_love_all(self):
        self.assertEqual(self.game.get_score(), "Love-All")

    def test_fifteen_all(self):
        self.play_points(1, 1)
        self.assertEqual(self.game.get_score(), "15-All")

    def test_thirty_all(self):
        self.play_points(2, 2)
        self.assertEqual(self.game.get_score(), "30-All")

    def test_deuce(self):
        self.play_points(3, 3)
        self.assertEqual(self.game.get_score(), "Deuce")
        
        # Vérification qu'un retour à deuce fonctionne
        self.play_points(1, 1)
        self.assertEqual(self.game.get_score(), "Deuce")

    def test_standard_scores(self):
        self.play_points(1, 0)
        self.assertEqual(self.game.get_score(), "15-Love")
        
        self.setUp()
        self.play_points(0, 2)
        self.assertEqual(self.game.get_score(), "Love-30")
        
        self.setUp()
        self.play_points(2, 3)
        self.assertEqual(self.game.get_score(), "30-40")

    def test_advantage_player_1(self):
        self.play_points(4, 3)
        self.assertEqual(self.game.get_score(), "Advantage Player 1")

    def test_advantage_player_2(self):
        self.play_points(3, 4)
        self.assertEqual(self.game.get_score(), "Advantage Player 2")

    def test_win_player_1(self):
        self.play_points(4, 0)
        self.assertEqual(self.game.get_score(), "Win for Player 1")
        
        self.setUp()
        self.play_points(5, 3)
        self.assertEqual(self.game.get_score(), "Win for Player 1")

    def test_win_player_2(self):
        self.play_points(1, 4)
        self.assertEqual(self.game.get_score(), "Win for Player 2")
        
        self.setUp()
        self.play_points(4, 6)
        self.assertEqual(self.game.get_score(), "Win for Player 2")

    def test_unknown_player_raises_error(self):
        with self.assertRaises(ValueError):
            self.game.won_point("Arbitre")

if __name__ == "__main__":
    unittest.main()