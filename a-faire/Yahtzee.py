"""
======================================================================
KATA : YAHTZEE
======================================================================

CONSIGNES :
Le jeu de Yahtzee est un jeu de dés simple. À chaque tour, le joueur 
lance 5 dés à 6 faces. Il doit ensuite placer son lancer dans une 
catégorie spécifique. Si le lancer correspond aux critères de la 
catégorie, le joueur marque des points selon les règles. Sinon, 
il marque 0 point.

L'objectif de ce kata est de créer les règles permettant de calculer 
le score d'un lancer pour n'importe quelle catégorie prédéfinie.

RÈGLES DES CATÉGORIES :
- Un, Deux, Trois, Quatre, Cinq, Six : Le joueur marque la somme des 
  dés affichant ce numéro. (ex: 1, 1, 2, 4, 4 placé sur "Quatre" donne 8).
- Paire (Pair) : La somme des 2 dés les plus élevés formant une paire. 
  (ex: 3, 3, 3, 4, 4 sur "Paire" donne 8).
- Double Paire (Two pairs) : S'il y a 2 paires différentes, la somme de 
  ces 4 dés. Sinon 0. (ex: 1, 1, 2, 3, 3 sur "Double Paire" donne 8).
- Brelan (Three of a kind) : S'il y a 3 dés identiques, la somme de 
  ces 3 dés. Sinon 0. (ex: 3, 3, 3, 4, 5 sur "Brelan" donne 9).
- Carré (Four of a kind) : S'il y a 4 dés identiques, la somme de 
  ces 4 dés. Sinon 0. (ex: 2, 2, 2, 2, 5 sur "Carré" donne 8).
- Petite Suite (Small straight) : Si les dés affichent 1, 2, 3, 4, 5, 
  le score est de 15. Sinon 0.
- Grande Suite (Large straight) : Si les dés affichent 2, 3, 4, 5, 6, 
  le score est de 20. Sinon 0.
- Full (Full house) : Si les dés forment un Brelan ET une Paire 
  (différente), la somme de tous les dés. (ex: 1,1,2,2,2 donne 8). 
  Attention: 4,4,4,4,4 n'est pas un Full.
- Yahtzee : Si les 5 dés sont identiques, le score est de 50. Sinon 0.
- Chance : La somme de tous les dés, peu importe leur valeur.
======================================================================
"""

import unittest
from collections import Counter

# --- CODE MÉTIER À TESTER ---
class Yahtzee:
    def __init__(self, d1, d2, d3, d4, d5):
        self.dice = [d1, d2, d3, d4, d5]
        self.counts = Counter(self.dice)

    def _sum_of_number(self, number):
        """Méthode utilitaire pour les catégories Un à Six"""
        return self.counts.get(number, 0) * number

    def ones(self):   return self._sum_of_number(1)
    def twos(self):   return self._sum_of_number(2)
    def threes(self): return self._sum_of_number(3)
    def fours(self):  return self._sum_of_number(4)
    def fives(self):  return self._sum_of_number(5)
    def sixes(self):  return self._sum_of_number(6)

    def pair(self):
        pairs = [val for val, count in self.counts.items() if count >= 2]
        return max(pairs) * 2 if pairs else 0

    def two_pairs(self):
        pairs = [val for val, count in self.counts.items() if count >= 2]
        if len(pairs) >= 2:
            # On trie pour prendre les deux paires les plus élevées s'il y en a 3 (impossible avec 5 dés, mais robuste)
            sorted_pairs = sorted(pairs, reverse=True)
            return sorted_pairs[0] * 2 + sorted_pairs[1] * 2
        return 0

    def three_of_a_kind(self):
        for val, count in self.counts.items():
            if count >= 3:
                return val * 3
        return 0

    def four_of_a_kind(self):
        for val, count in self.counts.items():
            if count >= 4:
                return val * 4
        return 0

    def small_straight(self):
        if set(self.dice) == {1, 2, 3, 4, 5}:
            return 15
        return 0

    def large_straight(self):
        if set(self.dice) == {2, 3, 4, 5, 6}:
            return 20
        return 0

    def full_house(self):
        # Un full requiert exactement une occurrence de 3 et une occurrence de 2
        if set(self.counts.values()) == {2, 3}:
            return sum(self.dice)
        return 0

    def yahtzee(self):
        if len(self.counts) == 1:
            return 50
        return 0

    def chance(self):
        return sum(self.dice)


# ======================================================================
# ZONE DE TESTS UNITAIRES
# ======================================================================
class TestYahtzee(unittest.TestCase):

    def test_chance_sums_all_dice(self):
        self.assertEqual(Yahtzee(2, 3, 4, 5, 1).chance(), 15)
        self.assertEqual(Yahtzee(3, 3, 4, 5, 1).chance(), 16)

    def test_yahtzee_scores_50_only_for_all_same_dice(self):
        self.assertEqual(Yahtzee(4, 4, 4, 4, 4).yahtzee(), 50)
        self.assertEqual(Yahtzee(6, 6, 6, 6, 6).yahtzee(), 50)
        self.assertEqual(Yahtzee(1, 1, 1, 2, 1).yahtzee(), 0)

    def test_ones_scores_sum_of_ones(self):
        self.assertEqual(Yahtzee(1, 2, 3, 4, 5).ones(), 1)
        self.assertEqual(Yahtzee(1, 2, 1, 4, 5).ones(), 2)
        self.assertEqual(Yahtzee(6, 2, 2, 4, 5).ones(), 0)

    def test_fours_scores_sum_of_fours(self):
        self.assertEqual(Yahtzee(1, 1, 2, 4, 4).fours(), 8)

    def test_pair_scores_highest_pair(self):
        self.assertEqual(Yahtzee(3, 4, 3, 5, 6).pair(), 6)
        # S'il y a deux paires, on prend la plus haute (4, 4)
        self.assertEqual(Yahtzee(3, 3, 3, 4, 4).pair(), 8)
        self.assertEqual(Yahtzee(1, 2, 3, 4, 5).pair(), 0)

    def test_two_pairs_scores_sum_of_the_two_pairs(self):
        self.assertEqual(Yahtzee(3, 3, 5, 4, 5).two_pairs(), 16)
        self.assertEqual(Yahtzee(3, 3, 3, 3, 5).two_pairs(), 0) # Pas deux paires distinctes

    def test_three_of_a_kind_scores_sum_of_the_three_dice(self):
        self.assertEqual(Yahtzee(3, 3, 3, 4, 5).three_of_a_kind(), 9)
        self.assertEqual(Yahtzee(5, 3, 5, 4, 5).three_of_a_kind(), 15)
        self.assertEqual(Yahtzee(3, 3, 4, 5, 6).three_of_a_kind(), 0)

    def test_four_of_a_kind_scores_sum_of_the_four_dice(self):
        self.assertEqual(Yahtzee(3, 3, 3, 3, 5).four_of_a_kind(), 12)
        self.assertEqual(Yahtzee(5, 5, 5, 4, 5).four_of_a_kind(), 20)
        self.assertEqual(Yahtzee(3, 3, 3, 4, 5).four_of_a_kind(), 0)

    def test_small_straight_scores_15(self):
        self.assertEqual(Yahtzee(1, 2, 3, 4, 5).small_straight(), 15)
        self.assertEqual(Yahtzee(2, 3, 4, 5, 1).small_straight(), 15) # Ordre sans importance
        self.assertEqual(Yahtzee(1, 2, 2, 4, 5).small_straight(), 0)

    def test_large_straight_scores_20(self):
        self.assertEqual(Yahtzee(2, 3, 4, 5, 6).large_straight(), 20)
        self.assertEqual(Yahtzee(3, 2, 4, 6, 5).large_straight(), 20)
        self.assertEqual(Yahtzee(1, 2, 3, 4, 5).large_straight(), 0)

    def test_full_house_scores_sum_of_all_dice(self):
        self.assertEqual(Yahtzee(6, 2, 2, 2, 6).full_house(), 18)
        self.assertEqual(Yahtzee(2, 3, 4, 5, 6).full_house(), 0)
        self.assertEqual(Yahtzee(4, 4, 4, 4, 4).full_house(), 0) # 5 identiques n'est pas un full


if __name__ == '__main__':
    unittest.main()