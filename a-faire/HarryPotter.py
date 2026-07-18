import unittest
from functools import lru_cache

# ==============================================================================
# CONSIGNES DU KATA : HARRY POTTER (CALCUL DE RÉDUCTIONS)
# ==============================================================================
# Contexte :
# Une librairie vend la série des livres Harry Potter (5 tomes différents).
# Chaque livre coûte 8 €. 
#
# Pour inciter les clients à acheter la série complète, une politique de 
# réduction est mise en place pour l'achat de livres *différents* :
# - 2 livres différents : 5% de réduction sur ces 2 livres
# - 3 livres différents : 10% de réduction sur ces 3 livres
# - 4 livres différents : 20% de réduction sur ces 4 livres
# - 5 livres différents : 25% de réduction sur ces 5 livres
#
# Le Piège (L'optimisation) :
# Le but de votre code est de calculer le prix le PLUS BAS possible pour 
# un panier donné. Attention à l'algorithme "glouton" ! 
# Par exemple, pour un panier contenant : 
# 2x Tome 1, 2x Tome 2, 2x Tome 3, 1x Tome 4, 1x Tome 5
# - Approche gloutonne (un groupe de 5 + un groupe de 3) : 
#   (5 * 8 * 0.75) + (3 * 8 * 0.90) = 30.00 + 21.60 = 51.60 €
# - Approche optimale (deux groupes de 4) :
#   (4 * 8 * 0.80) + (4 * 8 * 0.80) = 25.60 + 25.60 = 51.20 €
#
# Votre algorithme doit être assez intelligent pour trouver ce 51.20 €.
# ==============================================================================

class PotterPricer:
    # Constantes des règles métier
    BOOK_PRICE = 8.0
    # Dictionnaire des multiplicateurs de prix en fonction de la taille du groupe
    DISCOUNTS = {
        1: 1.0,   # Pas de réduction
        2: 0.95,  # 5% de réduction
        3: 0.90,  # 10% de réduction
        4: 0.80,  # 20% de réduction
        5: 0.75   # 25% de réduction
    }

    @staticmethod
    def calculate_price(basket: list[int]) -> float:
        """
        Calcule le prix optimal (le moins cher) pour un panier de livres.
        'basket' est une liste d'entiers représentant les IDs des livres (ex: [1, 1, 2, 3]).
        """
        if not basket:
            return 0.0

        # Étape 1 : Compter les occurrences de chaque livre
        counts = {}
        for book in basket:
            counts[book] = counts.get(book, 0) + 1
        
        # Nous n'avons besoin que des quantités (l'ID du livre importe peu pour le calcul).
        # On les trie de manière décroissante pour optimiser l'espace d'états de la mémoïsation.
        quantities = tuple(sorted(counts.values(), reverse=True))

        # Étape 2 : Exploration récursive des combinaisons possibles (Programmation Dynamique)
        @lru_cache(maxsize=None)
        def get_min_price(q_tuple: tuple) -> float:
            # Condition d'arrêt : plus aucun livre à traiter
            if not q_tuple:
                return 0.0
            
            num_unique_books = len(q_tuple)
            min_price = float('inf')
            
            # On essaie de former des groupes de tailles allant de 1 jusqu'au nombre max de livres différents
            for group_size in range(1, num_unique_books + 1):
                
                # On retire 1 exemplaire pour les 'group_size' premiers livres
                new_q = list(q_tuple)
                for i in range(group_size):
                    new_q[i] -= 1
                
                # On nettoie les livres dont le stock est tombé à 0 et on retrie le tuple
                new_q = tuple(sorted([count for count in new_q if count > 0], reverse=True))
                
                # Calcul du prix du groupe actuel
                group_price = group_size * PotterPricer.BOOK_PRICE * PotterPricer.DISCOUNTS[group_size]
                
                # Récursion pour le reste du panier
                current_price = group_price + get_min_price(new_q)
                
                # On conserve le prix le plus bas trouvé
                min_price = min(min_price, current_price)
                
            return min_price

        # Déclenchement de l'algorithme
        return get_min_price(quantities)


# ==============================================================================
# TESTS UNITAIRES
# ==============================================================================

class TestPotterKata(unittest.TestCase):

    def test_empty_basket(self):
        self.assertEqual(PotterPricer.calculate_price([]), 0.0)

    def test_single_books(self):
        self.assertEqual(PotterPricer.calculate_price([1]), 8.0)
        self.assertEqual(PotterPricer.calculate_price([2]), 8.0)
        self.assertEqual(PotterPricer.calculate_price([3]), 8.0)

    def test_multiple_identical_books(self):
        # 3 fois le même livre = pas de réduction
        self.assertEqual(PotterPricer.calculate_price([1, 1, 1]), 24.0)

    def test_simple_discounts(self):
        # 2 livres différents (5%)
        self.assertEqual(PotterPricer.calculate_price([1, 2]), 8.0 * 2 * 0.95)
        # 3 livres différents (10%)
        self.assertEqual(PotterPricer.calculate_price([1, 2, 3]), 8.0 * 3 * 0.90)
        # 4 livres différents (20%)
        self.assertEqual(PotterPricer.calculate_price([1, 2, 3, 4]), 8.0 * 4 * 0.80)
        # 5 livres différents (25%)
        self.assertEqual(PotterPricer.calculate_price([1, 2, 3, 4, 5]), 8.0 * 5 * 0.75)

    def test_mixed_basket(self):
        # 2 livres différents + 1 livre en double
        # Doit être calculé comme : (1 groupe de 2) + (1 groupe de 1)
        expected = (8 * 2 * 0.95) + 8.0
        self.assertEqual(PotterPricer.calculate_price([1, 1, 2]), expected)

    def test_edge_case_optimization(self):
        # Le fameux piège décrit dans l'énoncé !
        # Panier : 2xTome1, 2xTome2, 2xTome3, 1xTome4, 1xTome5
        basket = [1, 1, 2, 2, 3, 3, 4, 5]
        
        # Approche "Groupes 5 + 3" : 51.60
        # Approche "Groupes 4 + 4" : 51.20 (Doit gagner)
        self.assertEqual(PotterPricer.calculate_price(basket), 51.20)

    def test_extreme_basket(self):
        # Un panier beaucoup plus large pour tester les performances de la mémoïsation
        basket = (
            [1] * 5 + 
            [2] * 5 + 
            [3] * 4 + 
            [4] * 5 + 
            [5] * 4
        )
        # Doit faire 3 groupes de 5, et 2 groupes de 4
        expected = (3 * 8 * 5 * 0.75) + (2 * 8 * 4 * 0.80)
        self.assertEqual(PotterPricer.calculate_price(basket), expected)


if __name__ == '__main__':
    unittest.main()