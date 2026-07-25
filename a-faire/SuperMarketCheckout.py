import unittest
import math

# =============================================================================
# KATA : SUPERMARKET CHECKOUT (CAISSE DE SUPERMARCHÉ)
# =============================================================================
#
# CONSIGNES :
# L'objectif est de modéliser le processus de passage en caisse. Différents 
# articles ont des prix simples (1$ la boîte de soupe), mais il existe aussi 
# des promotions (2 achetées, la 3ème offerte) ou des prix au poids (1.99$/kg).
# 
# De plus, la caisse doit afficher le prix en temps réel au client. Si la 
# règle est "2 achetées, 1 offerte", le premier scan affichera 1.00$, le 
# second 1.00$, et le troisième 0.00$.
#
# Règles à implémenter :
# 1. Créez une classe `Checkout` avec une méthode `scan`.
# 2. `scan` accepte un SKU (identifiant) sous forme de chaîne et une quantité 
#    par défaut de 1.
# 3. La méthode doit pouvoir accepter une quantité entière personnalisée.
# 4. La méthode doit pouvoir accepter un poids (float/décimal).
# 5. Chaque `scan` doit retourner une chaîne de caractères pour affichage, 
#    incluant le SKU, la quantité (ou le poids), et le prix incrémental lié 
#    à ce scan.
# 6. Règles de tarification à respecter :
#
# | SKU    | Prix Unitaire | Règle de Volume                |
# |--------|---------------|--------------------------------|
# | SOUP   | $1.00         | 2 achetées, 1 gratuite         |
# | RAMEN  | $0.40         | 3 pour $1.00                   |
# | ORANGE | $2.00         | -                              |
# | GRAPES | $4 / lb       | -                              |
# | YOGURT | n/a           | 3 pour $2.00 (arrondis stricts)|
#
# Notes :
# - YOGURT : Le 1er coûte $0.67, le 2ème $0.67, et le 3ème $0.66 (total $2.00).
# - L'ordre des scans n'a pas d'importance. Ne présumez pas que les articles 
#   sont scannés en groupe ou en séquence.
# =============================================================================

class Checkout:
    def __init__(self):
        # Stocke les quantités entières scannées par SKU
        self.item_counts = {}
        # Stocke les poids totaux scannés par SKU
        self.item_weights = {}

    def scan(self, sku: str, quantity: int = 1, weight: float = None) -> str:
        """
        Enregistre un article et retourne la chaîne d'affichage avec le prix incrémental.
        """
        if weight is not None:
            # Gestion des articles vendus au poids (ex: GRAPES)
            old_weight = self.item_weights.get(sku, 0.0)
            new_weight = old_weight + weight
            self.item_weights[sku] = new_weight
            
            incremental_price = self._calculate_weight_price(sku, new_weight) - self._calculate_weight_price(sku, old_weight)
            return f"{sku} {weight} lbs : ${incremental_price:.2f}"
        else:
            # Gestion des articles vendus à l'unité
            old_count = self.item_counts.get(sku, 0)
            new_count = old_count + quantity
            self.item_counts[sku] = new_count
            
            incremental_price = self._calculate_unit_price(sku, new_count) - self._calculate_unit_price(sku, old_count)
            return f"{sku} x {quantity} : ${incremental_price:.2f}"

    def _calculate_unit_price(self, sku: str, count: int) -> float:
        """
        Calcule le prix total pour une quantité donnée d'un SKU.
        C'est ici que réside la logique métier des promotions.
        """
        if sku == "SOUP":
            # $1.00 l'unité. 2 achetées, 1 gratuite (par lots de 3, on en paie 2)
            payable_items = count - (count // 3)
            return payable_items * 1.00
            
        elif sku == "RAMEN":
            # $0.40 l'unité. 3 pour $1.00
            sets_of_three = count // 3
            remainder = count % 3
            return (sets_of_three * 1.00) + (remainder * 0.40)
            
        elif sku == "ORANGE":
            # $2.00 l'unité sans promotion
            return count * 2.00
            
        elif sku == "YOGURT":
            # 3 pour $2.00. 1er: $0.67, 2ème: $0.67, 3ème: $0.66
            sets_of_three = count // 3
            remainder = count % 3
            
            base_price = sets_of_three * 2.00
            if remainder == 1:
                return base_price + 0.67
            elif remainder == 2:
                return base_price + 1.34
            else:
                return base_price

        return 0.0

    def _calculate_weight_price(self, sku: str, weight: float) -> float:
        """Calcule le prix total pour un poids donné d'un SKU."""
        if sku == "GRAPES":
            return weight * 4.00
        return 0.0


# =============================================================================
# TESTS UNITAIRES
# =============================================================================

class TestSupermarketCheckout(unittest.TestCase):

    def setUp(self):
        """Initialise une nouvelle caisse avant chaque test."""
        self.checkout = Checkout()

    def test_scan_standard_item(self):
        """Teste un article basique sans promotion."""
        result = self.checkout.scan("ORANGE")
        self.assertEqual(result, "ORANGE x 1 : $2.00")
        
        result2 = self.checkout.scan("ORANGE", quantity=2)
        self.assertEqual(result2, "ORANGE x 2 : $4.00")

    def test_soup_buy_two_get_one_free(self):
        """Teste la règle SOUP : 2 achetées, 1 offerte."""
        self.assertEqual(self.checkout.scan("SOUP"), "SOUP x 1 : $1.00")
        self.assertEqual(self.checkout.scan("SOUP"), "SOUP x 1 : $1.00")
        # Le 3ème doit être gratuit
        self.assertEqual(self.checkout.scan("SOUP"), "SOUP x 1 : $0.00")
        # Le 4ème redevient payant
        self.assertEqual(self.checkout.scan("SOUP"), "SOUP x 1 : $1.00")

    def test_ramen_volume_pricing(self):
        """Teste la règle RAMEN : $0.40 l'unité, 3 pour $1.00."""
        self.assertEqual(self.checkout.scan("RAMEN"), "RAMEN x 1 : $0.40")
        self.assertEqual(self.checkout.scan("RAMEN"), "RAMEN x 1 : $0.40")
        # Le 3ème ne doit coûter que $0.20 pour atteindre le total de $1.00
        self.assertEqual(self.checkout.scan("RAMEN"), "RAMEN x 1 : $0.20")

    def test_yogurt_rounding_rules(self):
        """Teste la règle YOGURT avec les arrondis stricts (0.67, 0.67, 0.66)."""
        self.assertEqual(self.checkout.scan("YOGURT"), "YOGURT x 1 : $0.67")
        self.assertEqual(self.checkout.scan("YOGURT"), "YOGURT x 1 : $0.67")
        # Le 3ème doit coûter $0.66
        self.assertEqual(self.checkout.scan("YOGURT"), "YOGURT x 1 : $0.66")

    def test_grapes_by_weight(self):
        """Teste la tarification au poids pour les raisins."""
        self.assertEqual(self.checkout.scan("GRAPES", weight=0.5), "GRAPES 0.5 lbs : $2.00")
        self.assertEqual(self.checkout.scan("GRAPES", weight=2.0), "GRAPES 2.0 lbs : $8.00")

    def test_multiple_quantities_at_once(self):
        """Teste l'ajout de plusieurs articles en un seul scan avec des réductions immédiates."""
        # Ajouter 3 soupes d'un coup devrait coûter 2.00$
        self.assertEqual(self.checkout.scan("SOUP", quantity=3), "SOUP x 3 : $2.00")
        # Ajouter 4 ramens d'un coup devrait coûter 1.40$ (1 lot de 3 + 1 à l'unité)
        self.assertEqual(self.checkout.scan("RAMEN", quantity=4), "RAMEN x 4 : $1.40")

if __name__ == '__main__':
    unittest.main()