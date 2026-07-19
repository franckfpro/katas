import random
import unittest

# =============================================================================
# KATA : TRADING CARD GAME (Jeu de cartes à collectionner)
# =============================================================================
#
# CONSIGNES :
# Dans ce Kata, vous allez implémenter un jeu de cartes à 2 joueurs basique.
# Les règles s'inspirent vaguement de jeux comme Hearthstone ou Magic.
#
# Préparation :
# - Chaque joueur commence avec 30 PV (Points de Vie) et 0 emplacement de Mana.
# - Chaque joueur commence avec un deck de 20 cartes de Dégâts ayant les
#   coûts en Mana suivants : 0,0,1,1,2,2,2,3,3,3,3,4,4,4,5,5,6,6,7,8.
# - Chaque joueur tire 3 cartes aléatoires de son deck pour sa main de départ.
#
# Déroulement du jeu :
# - Le joueur actif reçoit 1 emplacement de Mana (jusqu'à un maximum de 10).
# - Les emplacements de Mana du joueur actif sont rechargés.
# - Le joueur actif tire une carte aléatoire de son deck.
# - Le joueur actif peut jouer autant de cartes qu'il peut se le permettre.
#   Toute carte jouée vide la quantité de Mana correspondante et inflige des
#   dégâts immédiats à l'adversaire égaux à son coût en Mana.
# - Si les PV de l'adversaire tombent à 0 ou moins, le joueur actif gagne.
# - Si le joueur actif ne peut pas (plus de cartes ou de Mana) ou ne veut
#   pas jouer d'autre carte, le tour passe à l'adversaire.
#
# Règles Spéciales :
# - Saignement (Bleeding Out) : Si le deck d'un joueur est vide, il reçoit
#   1 point de dégât au lieu de piocher une carte au début de son tour.
# - Surcharge (Overload) : Si un joueur pioche une carte et que sa main
#   dépasse 5 cartes, la carte piochée est défaussée au lieu d'être ajoutée.
# - Carte Nulle (Dud Card) : Les cartes à 0 Mana sont gratuites mais
#   n'infligent aucun dégât. Elles encombrent juste la main.
# =============================================================================

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 30
        self.mana_slots = 0
        self.active_mana = 0
        self.deck = [0, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 6, 6, 7, 8]
        self.hand = []
        random.shuffle(self.deck)

    def draw_initial_hand(self):
        """Pioche les 3 cartes de départ."""
        for _ in range(3):
            self.draw_card()

    def draw_card(self):
        """Pioche une carte avec gestion du Saignement et de la Surcharge."""
        if not self.deck:
            # Règle : Saignement (Bleeding Out)
            self.health -= 1
            return

        card = self.deck.pop(0)
        
        if len(self.hand) < 5:
            self.hand.append(card)
        # Règle : Surcharge (Overload) -> la carte est ignorée/défaussée si la main est pleine

    def prepare_turn(self):
        """Prépare le mana et pioche la carte du tour."""
        if self.mana_slots < 10:
            self.mana_slots += 1
        self.active_mana = self.mana_slots
        self.draw_card()


class Game:
    def __init__(self, player1_name="Joueur 1", player2_name="Joueur 2"):
        self.player1 = Player(player1_name)
        self.player2 = Player(player2_name)
        
        self.player1.draw_initial_hand()
        self.player2.draw_initial_hand()
        
        self.active_player = self.player1
        self.opponent = self.player2
        
        self.is_over = False
        self.winner = None

    def start_turn(self):
        """Démarre le tour du joueur actif."""
        if self.is_over:
            return
        
        self.active_player.prepare_turn()
        self._check_win_condition()

    def play_card(self, card_index):
        """Joue une carte de la main du joueur actif s'il a assez de mana."""
        if self.is_over:
            raise ValueError("La partie est déjà terminée.")
            
        if card_index < 0 or card_index >= len(self.active_player.hand):
            raise IndexError("Index de carte invalide.")

        card_cost = self.active_player.hand[card_index]

        if self.active_player.active_mana >= card_cost:
            # Consommer le mana
            self.active_player.active_mana -= card_cost
            # Infliger les dégâts
            self.opponent.health -= card_cost
            # Retirer la carte de la main
            self.active_player.hand.pop(card_index)
            
            self._check_win_condition()
        else:
            raise ValueError("Pas assez de mana pour jouer cette carte.")

    def end_turn(self):
        """Passe le tour à l'adversaire."""
        if not self.is_over:
            self.active_player, self.opponent = self.opponent, self.active_player
            self.start_turn()

    def _check_win_condition(self):
        """Vérifie si un joueur a perdu tous ses PV."""
        if self.player1.health <= 0 or self.player2.health <= 0:
            self.is_over = True
            if self.player1.health <= 0 and self.player2.health <= 0:
                self.winner = "Match Nul"
            elif self.player1.health <= 0:
                self.winner = self.player2.name
            else:
                self.winner = self.player1.name


# =============================================================================
# TESTS UNITAIRES
# =============================================================================

class TestTradingCardGame(unittest.TestCase):

    def setUp(self):
        """Initialise une nouvelle partie avant chaque test."""
        self.game = Game("Alice", "Bob")

    def test_initial_state(self):
        """Vérifie que les joueurs commencent avec 30 PV, 0 Mana et 3 cartes."""
        self.assertEqual(self.game.player1.health, 30)
        self.assertEqual(self.game.player1.mana_slots, 0)
        self.assertEqual(len(self.game.player1.hand), 3)
        self.assertEqual(len(self.game.player1.deck), 17) # 20 - 3

    def test_turn_preparation(self):
        """Vérifie le gain de mana et la pioche au début du tour."""
        self.game.start_turn()
        
        self.assertEqual(self.game.active_player.mana_slots, 1)
        self.assertEqual(self.game.active_player.active_mana, 1)
        self.assertEqual(len(self.game.active_player.hand), 4)

    def test_max_mana_slots(self):
        """Vérifie que le maximum d'emplacements de mana est de 10."""
        self.game.active_player.mana_slots = 9
        self.game.start_turn()
        self.assertEqual(self.game.active_player.mana_slots, 10)
        
        # Le tour suivant, ça ne doit pas dépasser 10
        self.game.end_turn()
        self.game.end_turn()
        self.assertEqual(self.game.active_player.mana_slots, 10)

    def test_overload_rule(self):
        """Vérifie la surcharge : pas plus de 5 cartes en main."""
        self.game.active_player.hand = [1, 2, 3, 4, 5]
        deck_size_before = len(self.game.active_player.deck)
        
        self.game.start_turn() # Devrait piocher et défausser
        
        self.assertEqual(len(self.game.active_player.hand), 5)
        self.assertEqual(len(self.game.active_player.deck), deck_size_before - 1)

    def test_bleeding_out_rule(self):
        """Vérifie le saignement : dégâts si le deck est vide."""
        self.game.active_player.deck = []
        health_before = self.game.active_player.health
        
        self.game.start_turn()
        
        self.assertEqual(self.game.active_player.health, health_before - 1)

    def test_play_card_success(self):
        """Vérifie que jouer une carte coûte du mana et inflige des dégâts."""
        self.game.start_turn()
        
        # Forçons la main et le mana pour le test
        self.game.active_player.active_mana = 5
        self.game.active_player.hand = [4, 1]
        
        opponent_health_before = self.game.opponent.health
        
        self.game.play_card(0) # Joue la carte coûtant 4
        
        self.assertEqual(self.game.active_player.active_mana, 1)
        self.assertEqual(len(self.game.active_player.hand), 1)
        self.assertEqual(self.game.opponent.health, opponent_health_before - 4)

    def test_play_card_insufficient_mana(self):
        """Vérifie qu'on ne peut pas jouer une carte trop chère."""
        self.game.start_turn()
        
        self.game.active_player.active_mana = 2
        self.game.active_player.hand = [5]
        
        with self.assertRaises(ValueError):
            self.game.play_card(0)

    def test_win_condition(self):
        """Vérifie que le jeu se termine quand les PV tombent à 0."""
        self.game.start_turn()
        
        self.game.active_player.active_mana = 10
        self.game.active_player.hand = [30] # Carte fictive pour tuer en un coup
        
        self.game.play_card(0)
        
        self.assertTrue(self.game.is_over)
        self.assertEqual(self.game.winner, self.game.active_player.name)

if __name__ == '__main__':
    unittest.main()