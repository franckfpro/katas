"""
======================================================================
KATA : WALLET (Portefeuille)
======================================================================

CONSIGNES :
Étant donné un portefeuille (Wallet) contenant des actions (Stocks), 
construisez une fonction qui calcule la valeur du portefeuille dans 
une devise (Currency) donnée.

- Les actions ont une quantité (quantity) et un type (StockType). 
- Le StockType peut être, par exemple : pétrole (petroleum), Euros, 
  bitcoins ou Dollars.
- Pour évaluer le portefeuille dans une devise, vous devez utiliser 
  un fournisseur externe (API) pour obtenir les taux de change.
- Exemples d'API de taux suggérées (pour information) :
  http://api.fixer.io/ ou https://finance.google.com/

L'approche choisie ici :
Pour rendre notre code testable (Test-Driven Development), nous allons 
injecter le fournisseur de taux de change (rate_provider) sous la forme 
d'une fonction (Callable). Ainsi, dans nos tests unitaires, nous pourrons 
passer un faux fournisseur (stub) pour contrôler les taux sans faire de 
véritables appels HTTP !
======================================================================
"""

import unittest
from enum import Enum
from typing import List, Callable

# --- ENTITÉS DU DOMAINE ---

class StockType(Enum):
    PETROLEUM = "PETROLEUM"
    BITCOIN = "BITCOIN"
    USD = "USD"
    EUR = "EUR"

class Currency(Enum):
    EUR = "EUR"
    USD = "USD"

class Stock:
    def __init__(self, quantity: float, stock_type: StockType):
        self.quantity = quantity
        self.stock_type = stock_type

class Wallet:
    def __init__(self):
        self.stocks: List[Stock] = []

    def add_stock(self, stock: Stock):
        """Ajoute une action au portefeuille."""
        self.stocks.append(stock)

    def value(self, currency: Currency, rate_provider: Callable[[StockType, Currency], float]) -> float:
        """
        Calcule la valeur totale du portefeuille dans la devise demandée.
        Le paramètre `rate_provider` est une fonction injectée qui retourne 
        le taux de conversion.
        """
        total_value = 0.0
        for stock in self.stocks:
            # On interroge le fournisseur de taux injecté
            rate = rate_provider(stock.stock_type, currency)
            total_value += stock.quantity * rate
            
        return total_value


# ======================================================================
# ZONE DE TESTS UNITAIRES
# ======================================================================
class TestWallet(unittest.TestCase):
    
    def setUp(self):
        self.wallet = Wallet()

    def stub_rate_provider(self, stock_type: StockType, currency: Currency) -> float:
        """
        Faux fournisseur de taux (Stub) utilisé uniquement pour les tests.
        Il évite de faire de vrais appels réseau et retourne des valeurs fixes.
        """
        rates = {
            (StockType.PETROLEUM, Currency.EUR): 50.0,    # 1 baril = 50 EUR
            (StockType.BITCOIN, Currency.EUR): 30000.0,   # 1 BTC = 30000 EUR
            (StockType.USD, Currency.EUR): 0.90,          # 1 USD = 0.90 EUR
            (StockType.EUR, Currency.EUR): 1.0,           # 1 EUR = 1 EUR
        }
        # Retourne le taux si trouvé, sinon 0.0
        return rates.get((stock_type, currency), 0.0)

    # --- TESTS ---

    def test_empty_wallet_value_is_zero(self):
        result = self.wallet.value(Currency.EUR, self.stub_rate_provider)
        self.assertEqual(result, 0.0)

    def test_wallet_value_with_single_stock(self):
        self.wallet.add_stock(Stock(2.0, StockType.PETROLEUM))
        
        # 2 barils * 50 EUR = 100 EUR
        result = self.wallet.value(Currency.EUR, self.stub_rate_provider)
        self.assertEqual(result, 100.0)

    def test_wallet_value_with_multiple_stocks(self):
        self.wallet.add_stock(Stock(2.0, StockType.PETROLEUM))  # 100 EUR
        self.wallet.add_stock(Stock(0.5, StockType.BITCOIN))    # 15000 EUR
        self.wallet.add_stock(Stock(100.0, StockType.USD))      # 90 EUR
        self.wallet.add_stock(Stock(10.0, StockType.EUR))       # 10 EUR
        
        expected_total = 100.0 + 15000.0 + 90.0 + 10.0
        result = self.wallet.value(Currency.EUR, self.stub_rate_provider)
        
        self.assertEqual(result, expected_total)

    def test_wallet_with_unknown_rate_defaults_to_zero(self):
        # Si on demande une devise que le stub ne connaît pas (ex: USD)
        self.wallet.add_stock(Stock(2.0, StockType.PETROLEUM))
        
        result = self.wallet.value(Currency.USD, self.stub_rate_provider)
        self.assertEqual(result, 0.0)


if __name__ == '__main__':
    unittest.main()