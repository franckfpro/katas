import unittest
from dataclasses import dataclass
from typing import List, Any

# ==============================================================================
# CONSIGNES DU KATA (Traduites en Français)
# ==============================================================================
"""
Contexte :
Vous écrivez un logiciel qui doit afficher les joueurs sur un tableau des scores 
(leader board). Chaque ligne du tableau doit inclure le classement général du joueur 
(son rang), son nom et son score. Pour cet exercice, les scores les plus élevés 
sont les meilleurs. Le joueur avec le score le plus élevé doit être en première 
position avec un rang de 1 (le classement ne commence pas à 0).

Instructions :
Créer un service avec une méthode qui accepte une liste de joueurs avec leurs 
scores respectifs et produit les données nécessaires pour un tableau des scores 
(rang, nom, score).
1. Commencez par tester que le comportement de base est correct lorsqu'il n'y a 
   pas de scores en double.
2. Lorsque des scores en double existent, une égalité se produit. Les joueurs à 
   égalité reçoivent le même rang. Cependant, le joueur suivant après l'égalité 
   aura un rang basé sur le nombre total de joueurs au-dessus de lui. 
   Par exemple :
   | Nom       | Score |
   | Ardalis   | 10    |
   | Bob       | 8     |
   | Chrissy   | 8     |
   | Doris     | 7     |
   Les rangs seraient : 1, 2, 2, 4.
3. En cas d'égalité de rang, les joueurs doivent être triés par ordre 
   alphabétique de leur nom.

Bonus (Extra Credit) :
1. Parfois, les scores les plus bas sont les meilleurs (comme au golf ou pour 
   des temps de course). Configurez votre service pour qu'il puisse classer du 
   score le plus bas au plus élevé. Le tri alphabétique en cas d'égalité ne 
   doit pas changer.
2. Assurez-vous que votre service fonctionne avec des types de données arbitraires 
   pour le score, à condition qu'ils soient comparables (ex: float, int, etc.).
"""

# ==============================================================================
# VOTRE IMPLEMENTATION (Le Kata à résoudre)
# ==============================================================================

@dataclass
class Player:
    name: str
    score: Any  # Type Any pour permettre des entiers, flottants, etc.

@dataclass
class RankedPlayer:
    rank: int
    name: str
    score: Any


class LeaderboardService:
    def __init__(self, highest_is_best: bool = True):
        """
        Initialise le service de classement.
        :param highest_is_best: Si True, le score le plus haut est le meilleur.
                                Si False, le score le plus bas est le meilleur.
        """
        self.highest_is_best = highest_is_best

    def get_leaderboard(self, players: List[Player]) -> List[RankedPlayer]:
        if not players:
            return []

        # Tri des joueurs :
        # En Python, le tri (sort) est stable. Nous pouvons donc trier d'abord
        # par ordre alphabétique croissant, puis par score.
        sorted_players = sorted(players, key=lambda p: p.name)
        sorted_players.sort(key=lambda p: p.score, reverse=self.highest_is_best)

        leaderboard = []
        current_rank = 1
        players_processed = 0
        previous_score = None

        for player in sorted_players:
            players_processed += 1
            
            # Si le score change par rapport au précédent, le rang est mis à jour
            # pour correspondre au nombre de joueurs déjà traités.
            if previous_score is None or player.score != previous_score:
                current_rank = players_processed

            leaderboard.append(RankedPlayer(current_rank, player.name, player.score))
            previous_score = player.score

        return leaderboard


# ==============================================================================
# TESTS UNITAIRES (Validation du comportement)
# ==============================================================================

class TestLeaderboardService(unittest.TestCase):

    def test_unique_scores_highest_is_best(self):
        """Doit classer correctement des scores uniques du plus haut au plus bas."""
        players = [
            Player("Bob", 8),
            Player("Ardalis", 10),
            Player("Doris", 7)
        ]
        service = LeaderboardService(highest_is_best=True)
        board = service.get_leaderboard(players)

        self.assertEqual(len(board), 3)
        self.assertEqual(board[0], RankedPlayer(1, "Ardalis", 10))
        self.assertEqual(board[1], RankedPlayer(2, "Bob", 8))
        self.assertEqual(board[2], RankedPlayer(3, "Doris", 7))

    def test_duplicate_scores_with_ties(self):
        """Doit gérer les égalités (rangs 1, 2, 2, 4) et trier par nom alphabétique."""
        players = [
            Player("Chrissy", 8),
            Player("Ardalis", 10),
            Player("Bob", 8),
            Player("Doris", 7)
        ]
        service = LeaderboardService(highest_is_best=True)
        board = service.get_leaderboard(players)

        self.assertEqual(board[0], RankedPlayer(1, "Ardalis", 10))
        # Bob et Chrissy sont ex aequo. Bob est devant grâce à l'ordre alphabétique.
        self.assertEqual(board[1], RankedPlayer(2, "Bob", 8))
        self.assertEqual(board[2], RankedPlayer(2, "Chrissy", 8))
        # Doris arrive à la 4ème place (car 3 joueurs sont devant elle).
        self.assertEqual(board[3], RankedPlayer(4, "Doris", 7))

    def test_lowest_is_best_golf_scenario(self):
        """Doit classer du plus petit score au plus grand si paramétré ainsi (ex: Golf)."""
        players = [
            Player("Tiger", 70),
            Player("Rory", 72),
            Player("Phil", 72),
            Player("Bubba", 75)
        ]
        service = LeaderboardService(highest_is_best=False)
        board = service.get_leaderboard(players)

        self.assertEqual(board[0], RankedPlayer(1, "Tiger", 70))
        # Phil avant Rory par ordre alphabétique
        self.assertEqual(board[1], RankedPlayer(2, "Phil", 72))
        self.assertEqual(board[2], RankedPlayer(2, "Rory", 72))
        self.assertEqual(board[3], RankedPlayer(4, "Bubba", 75))

    def test_arbitrary_types_for_scores(self):
        """Doit fonctionner avec d'autres types comparables, comme des flottants (temps de course)."""
        players = [
            Player("Usain", 9.58),
            Player("Tyson", 9.69),
            Player("Yohan", 9.69),
            Player("Justin", 9.74)
        ]
        service = LeaderboardService(highest_is_best=False)
        board = service.get_leaderboard(players)

        self.assertEqual(board[0], RankedPlayer(1, "Usain", 9.58))
        self.assertEqual(board[1], RankedPlayer(2, "Tyson", 9.69))
        self.assertEqual(board[2], RankedPlayer(2, "Yohan", 9.69))
        self.assertEqual(board[3], RankedPlayer(4, "Justin", 9.74))


if __name__ == '__main__':
    unittest.main()