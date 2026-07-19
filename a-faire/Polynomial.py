import unittest

"""
KATA POLYNOMIAL PRETTY PRINT
============================

Description :
Il s'agit d'afficher le plus joliment possible un polynôme à coefficients 
entiers. Le polynôme est représenté par une suite d'entiers (une liste), 
où l'index correspond au degré du monôme.

Règles d'usage :
1. Les monômes sont affichés du degré fort vers les degrés faibles.
2. Un monôme à coefficient nul n'est affiché que pour le polynôme nul = 0.
3. Un monôme avec un coefficient de 1 n'affiche ce coefficient que pour le degré 0.
4. Les exposants donnent l'affichage :
   - "rien" si l'exposant est nul
   - "x" si l'exposant est égal à 1
   - "x^n" pour les autres
5. Les opérateurs + et - séparent les monômes. Les coefficients négatifs 
   n'apparaissent avec le signe collé que s'ils sont en tête de la représentation.
"""

def print_polynomial(coeffs: list[int]) -> str:
    """
    Formate une liste de coefficients en une chaîne de caractères représentant le polynôme.
    L'index de l'élément dans la liste correspond à la puissance de x.
    """
    # Règle 2 : Polynôme nul
    if not coeffs or all(c == 0 for c in coeffs):
        return "0"
        
    result = []
    is_first = True
    
    # Règle 1 : Parcours du degré fort vers le degré faible
    for i in range(len(coeffs) - 1, -1, -1):
        c = coeffs[i]
        
        # Ignorer les coefficients nuls
        if c == 0:
            continue
            
        term = ""
        
        # Règle 5 : Gestion des opérateurs et des signes
        if is_first:
            if c < 0:
                term += "-"
        else:
            if c < 0:
                result.append(" - ")
            else:
                result.append(" + ")
                
        # Règle 3 : Gestion de l'affichage du coefficient 1
        abs_c = abs(c)
        if i == 0 or abs_c != 1:
            term += str(abs_c)
            
        # Règle 4 : Gestion de la variable et de l'exposant
        if i == 1:
            term += "x"
        elif i > 1:
            term += f"x^{i}"
            
        result.append(term)
        is_first = False
        
    return "".join(result)


class TestPolynomialPrettyPrint(unittest.TestCase):
    
    def test_zero_polynomial(self):
        self.assertEqual(print_polynomial([]), "0")
        self.assertEqual(print_polynomial([0]), "0")
        self.assertEqual(print_polynomial([0, 0, 0]), "0")
        
    def test_single_constant(self):
        self.assertEqual(print_polynomial([5]), "5")
        self.assertEqual(print_polynomial([-3]), "-3")
        self.assertEqual(print_polynomial([1]), "1")
        
    def test_degree_one(self):
        self.assertEqual(print_polynomial([0, 1]), "x")
        self.assertEqual(print_polynomial([0, -1]), "-x")
        self.assertEqual(print_polynomial([0, 5]), "5x")
        self.assertEqual(print_polynomial([0, -5]), "-5x")
        
    def test_degree_n(self):
        self.assertEqual(print_polynomial([0, 0, 1]), "x^2")
        self.assertEqual(print_polynomial([0, 0, -1]), "-x^2")
        self.assertEqual(print_polynomial([0, 0, 4]), "4x^2")
        
    def test_multiple_terms(self):
        # 1 + x (doit s'afficher x + 1)
        self.assertEqual(print_polynomial([1, 1]), "x + 1")
        # 5 - 3x^2
        self.assertEqual(print_polynomial([5, 0, -3]), "-3x^2 + 5")
        # -2 + x - x^2 + 4x^3
        self.assertEqual(print_polynomial([-2, 1, -1, 4]), "4x^3 - x^2 + x - 2")
        
    def test_operator_formatting(self):
        # Vérifie l'espacement autour des opérateurs pour les termes non initiaux
        self.assertEqual(print_polynomial([1, 1, 1]), "x^2 + x + 1")
        self.assertEqual(print_polynomial([-1, -1, -1]), "-x^2 - x - 1")

if __name__ == '__main__':
    unittest.main()