import unittest
from collections import Counter

"""
KATA POKER HANDS
================

Description :
Votre tâche consiste à comparer plusieurs paires de mains de poker et à 
indiquer laquelle a le rang le plus élevé.

Règles du Poker :
Un paquet de poker contient 52 cartes - chaque carte a une "couleur" (Trèfle/Clubs, 
Carreau/Diamonds, Cœur/Hearts, ou Pique/Spades, notées C, D, H, S) et une "valeur" 
(2, 3, 4, 5, 6, 7, 8, 9, 10, Valet, Reine, Roi, As, notées 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A). 
L'As est la valeur la plus forte, le 2 la plus faible. Les couleurs n'ont pas d'ordre de valeur.

Une main de poker est constituée de 5 cartes. Les mains sont classées de la plus 
faible à la plus forte selon l'ordre partiel suivant :

1. Carte Haute (High Card) : La main de rang le plus bas. Départagée par la valeur 
   de la carte la plus haute, puis la suivante, etc.
2. Paire (Pair) : 2 cartes de même valeur. Départagée par la valeur de la paire, 
   puis par les cartes restantes dans l'ordre décroissant.
3. Double Paire (Two Pairs) : 2 paires différentes. Départagée par la paire la plus haute, 
   puis la deuxième, puis la carte restante.
4. Brelan (Three of a Kind) : 3 cartes de même valeur. Départagée par la valeur du brelan.
5. Suite (Straight) : 5 cartes aux valeurs consécutives. Départagée par la carte la plus haute.
6. Couleur (Flush) : 5 cartes de la même couleur (suit). Départagée comme la "Carte Haute".
7. Full (Full House) : Un brelan et une paire. Départagée par la valeur du brelan.
8. Carré (Four of a Kind) : 4 cartes de même valeur. Départagée par la valeur du carré.
9. Quinte Flush (Straight Flush) : 5 cartes consécutives de la même couleur. 
   Départagée par la carte la plus haute.
"""

def evaluate_hand(hand_string):
    """
    Évalue une main de poker de 5 cartes et retourne un tuple représentant sa force.
    Le premier élément du tuple est le rang de la combinaison (0 à 8).
    Les éléments suivants sont les valeurs des cartes triées par importance pour départager.
    """
    value_dict = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
                  'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    
    cards = hand_string.split()
    # Extraction et tri décroissant des valeurs
    values = sorted([value_dict[card[0]] for card in cards], reverse=True)
    suits = [card[1] for card in cards]
    
    # Vérification de Couleur (Flush) et Suite (Straight)
    is_flush = len(set(suits)) == 1
    is_straight = len(set(values)) == 5 and (values[0] - values[-1] == 4)
    
    # Comptage des occurrences (ex: Brelan = 3, Paire = 2)
    counts = Counter(values)
    # Tri par fréquence d'apparition d'abord, puis par valeur de la carte
    sorted_counts = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)
    
    frequencies = [item[1] for item in sorted_counts]
    ordered_values = [item[0] for item in sorted_counts]
    
    # Détermination du rang de la main (0 à 8)
    if is_straight and is_flush:
        rank = 8 # Quinte Flush
    elif frequencies == [4, 1]:
        rank = 7 # Carré
    elif frequencies == [3, 2]:
        rank = 6 # Full
    elif is_flush:
        rank = 5 # Couleur
    elif is_straight:
        rank = 4 # Suite
    elif frequencies == [3, 1, 1]:
        rank = 3 # Brelan
    elif frequencies == [2, 2, 1]:
        rank = 2 # Double Paire
    elif frequencies == [2, 1, 1, 1]:
        rank = 1 # Paire
    else:
        rank = 0 # Carte Haute
        
    return (rank, ordered_values)

def compare_hands(black_hand, white_hand):
    """
    Compare deux mains et retourne le gagnant ou 'Tie' (Égalité).
    """
    black_score = evaluate_hand(black_hand)
    white_score = evaluate_hand(white_hand)
    
    if black_score > white_score:
        return "Black wins."
    elif white_score > black_score:
        return "White wins."
    else:
        return "Tie."


class TestPokerHands(unittest.TestCase):
    
    def test_high_card_white_wins(self):
        # White a un As, Black a un Roi
        self.assertEqual(compare_hands("2H 3D 5S 9C KD", "2C 3H 4S 8C AH"), "White wins.")
        
    def test_high_card_black_wins_on_tiebreaker(self):
        # Les deux ont un As, mais Black a un 9 contre un 8 pour White
        self.assertEqual(compare_hands("2H 3D 5S 9C AH", "2C 3H 4S 8C AD"), "Black wins.")
        
    def test_pair_beats_high_card(self):
        # Black a une paire de 2, White a une carte haute (As)
        self.assertEqual(compare_hands("2H 2D 5S 9C KD", "2C 3H 4S 8C AH"), "Black wins.")
        
    def test_two_pairs_beat_pair(self):
        self.assertEqual(compare_hands("2H 2D 5S 5C KD", "3C 3H 4S 8C AH"), "Black wins.")
        
    def test_three_of_a_kind_beats_two_pairs(self):
        self.assertEqual(compare_hands("2H 2D 2S 5C KD", "3C 3H 4S 4C AH"), "Black wins.")
        
    def test_full_house_beats_flush(self):
        # Black a un Full (44422), White a une couleur à Pique
        self.assertEqual(compare_hands("2H 4S 4C 2D 4H", "2S 8S AS QS 3S"), "Black wins.")
        
    def test_straight_beats_three_of_a_kind(self):
        self.assertEqual(compare_hands("2H 3D 4S 5C 6D", "9C 9H 9S 8C AH"), "Black wins.")
        
    def test_straight_flush_beats_four_of_a_kind(self):
        self.assertEqual(compare_hands("8H 9H TH JH QH", "9C 9D 9S 9H AH"), "Black wins.")
        
    def test_tie(self):
        self.assertEqual(compare_hands("2H 3D 5S 9C KD", "2D 3H 5C 9S KH"), "Tie.")
        
    def test_highest_pair_wins(self):
        # Black a une paire de Valets, White a une paire de Dames
        self.assertEqual(compare_hands("JH JD 5S 9C KD", "QC QH 4S 8C AH"), "White wins.")

if __name__ == '__main__':
    unittest.main()