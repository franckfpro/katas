"""
Kata Jeu de Nim (Nim Game) - Consignes

Le jeu de Nim est un jeu de stratégie classique à deux joueurs.
Il existe plusieurs variantes (notamment avec plusieurs rangées), mais nous 
allons implémenter ici la version avec une seule pile (le jeu de soustraction).

Objectif :
- Développer un jeu de Nim jouable à deux joueurs.
- Le jeu commence par défaut avec 10 bâtonnets.
- À tour de rôle, chaque joueur peut retirer 1, 2 ou 3 bâtonnets.
- Le joueur qui retire le dernier bâtonnet remporte la partie (variante "Normale").

Bonus (implémentés ici pour un code flexible) :
- Permettre de configurer le nombre de bâtonnets de départ.
- Permettre de configurer le nom des joueurs.
- Sécuriser les entrées (empêcher de retirer 0, un nombre négatif, ou plus de 
  bâtonnets qu'il n'en reste).
"""

import unittest

class NimGame:
    def __init__(self, initial_sticks=10, max_take=3, player1="Joueur 1", player2="Joueur 2"):
        if initial_sticks <= 0:
            raise ValueError("Le jeu doit commencer avec au moins 1 bâtonnet.")
        
        self.sticks = initial_sticks
        self.max_take = max_take
        self.players = [player1, player2]
        self.current_player_index = 0
        self.winner = None

    def play_turn(self, amount):
        """
        Exécute le tour du joueur courant.
        """
        if self.is_game_over():
            raise ValueError("La partie est déjà terminée.")
            
        if amount < 1 or amount > self.max_take:
            raise ValueError(f"Action invalide : vous devez retirer entre 1 et {self.max_take} bâtonnet(s).")
            
        if amount > self.sticks:
            raise ValueError(f"Action invalide : il ne reste que {self.sticks} bâtonnet(s).")

        # Mise à jour de l'état
        self.sticks -= amount

        # Vérification de la condition de victoire
        if self.sticks == 0:
            self.winner = self.get_current_player()
        else:
            # Passage au joueur suivant
            self.current_player_index = 1 - self.current_player_index

    def get_current_player(self):
        """Retourne le nom du joueur dont c'est le tour."""
        return self.players[self.current_player_index]

    def is_game_over(self):
        """Indique si la partie est terminée."""
        return self.winner is not None


# ==========================================
# SUITE DE TESTS UNITAIRES
# ==========================================

class TestNimGame(unittest.TestCase):

    def test_initial_state(self):
        game = NimGame()
        self.assertEqual(game.sticks, 10)
        self.assertEqual(game.get_current_player(), "Joueur 1")
        self.assertFalse(game.is_game_over())
        self.assertIsNone(game.winner)

    def test_custom_setup(self):
        game = NimGame(initial_sticks=15, player1="Alice", player2="Bob")
        self.assertEqual(game.sticks, 15)
        self.assertEqual(game.get_current_player(), "Alice")

    def test_valid_turn_alternation(self):
        game = NimGame()
        game.play_turn(2) # Joueur 1 retire 2
        self.assertEqual(game.sticks, 8)
        self.assertEqual(game.get_current_player(), "Joueur 2")
        
        game.play_turn(3) # Joueur 2 retire 3
        self.assertEqual(game.sticks, 5)
        self.assertEqual(game.get_current_player(), "Joueur 1")

    def test_invalid_turn_amount(self):
        game = NimGame()
        # Ne peut pas retirer 0
        with self.assertRaises(ValueError):
            game.play_turn(0)
            
        # Ne peut pas retirer plus que le maximum autorisé (3 par défaut)
        with self.assertRaises(ValueError):
            game.play_turn(4)
            
        # Ne peut pas retirer un nombre négatif
        with self.assertRaises(ValueError):
            game.play_turn(-1)

    def test_cannot_take_more_than_remaining(self):
        game = NimGame(initial_sticks=2)
        with self.assertRaises(ValueError):
            game.play_turn(3) # Essaie de prendre 3 alors qu'il n'en reste que 2

    def test_game_victory(self):
        game = NimGame(initial_sticks=4, player1="Alice", player2="Bob")
        game.play_turn(1) # Alice laisse 3
        self.assertEqual(game.get_current_player(), "Bob")
        
        game.play_turn(3) # Bob prend les 3 derniers
        
        self.assertEqual(game.sticks, 0)
        self.assertTrue(game.is_game_over())
        self.assertEqual(game.winner, "Bob")

    def test_cannot_play_after_game_over(self):
        game = NimGame(initial_sticks=2)
        game.play_turn(2) # Victoire
        
        with self.assertRaises(ValueError):
            game.play_turn(1)


if __name__ == '__main__':
    unittest.main()