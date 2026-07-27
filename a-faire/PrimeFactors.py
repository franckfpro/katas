import unittest

"""
KATA PRIME FACTORS (FACTEURS PREMIERS)
======================================

Description :
Écrivez une fonction (ou une classe contenant une méthode statique) qui génère 
les facteurs premiers d'un nombre donné. 

Règles :
- La fonction prend un entier en argument.
- Elle retourne une collection (liste) d'entiers.
- Cette collection contient les facteurs premiers de l'argument d'entrée, 
  dans l'ordre croissant.
- Écrivez une suite de tests pour valider cette fonctionnalité de manière itérative.

Indice : 
Votre tout premier test devrait confirmer que, pour une entrée de 1, 
la fonction retourne une collection vide.

Ressources :
Ce kata est un classique souvent utilisé par "Uncle Bob" Martin pour 
démontrer l'efficacité du Développement Dirigé par les Tests (TDD).
"""

def generate_prime_factors(n: int) -> list[int]:
    """
    Génère les facteurs premiers d'un entier n donné.
    Retourne une liste d'entiers ordonnée.
    """
    factors = []
    divisor = 2
    
    # On divise n par le diviseur tant que le reste est 0
    # On incrémente le diviseur lorsque n n'est plus divisible par celui-ci
    while n > 1:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 1
        
    return factors


class TestPrimeFactors(unittest.TestCase):
    
    def test_one_returns_empty_list(self):
        # 1 n'a pas de facteurs premiers
        self.assertEqual(generate_prime_factors(1), [])
        
    def test_two_returns_two(self):
        self.assertEqual(generate_prime_factors(2), [2])
        
    def test_three_returns_three(self):
        self.assertEqual(generate_prime_factors(3), [3])
        
    def test_four_returns_two_and_two(self):
        self.assertEqual(generate_prime_factors(4), [2, 2])
        
    def test_six_returns_two_and_three(self):
        self.assertEqual(generate_prime_factors(6), [2, 3])
        
    def test_eight_returns_two_two_two(self):
        self.assertEqual(generate_prime_factors(8), [2, 2, 2])
        
    def test_nine_returns_three_three(self):
        self.assertEqual(generate_prime_factors(9), [3, 3])
        
    def test_large_number(self):
        # 3 * 5 * 7 * 11 * 11 = 12705
        self.assertEqual(generate_prime_factors(12705), [3, 5, 7, 11, 11])

if __name__ == '__main__':
    unittest.main()