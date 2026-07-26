import unittest
import math

# ==============================================================================
# KATA : RPN CALCULATOR (Calculatrice NPI)
# ==============================================================================
#
# CONSIGNES :
# Une calculatrice NPI évalue des expressions écrites en Notation Polonaise Inverse 
# (Reverse Polish Notation).
# 
# Une expression NPI (ou expression postfixée) est définie comme suit :
# - Un nombre X : dans ce cas, la valeur de l'expression est celle de X.
# - Une séquence de la forme "E1 E2 OP", où E1 et E2 sont des expressions NPI 
#   et OP est une opération arithmétique.
#
# Le but du kata est d'implémenter l'évaluation d'une chaîne de caractères 
# représentant une expression NPI.
#
# Vous devez supporter :
# 1. Les opérateurs arithmétiques de base (+, -, *, /)
# 2. L'opération SQRT (racine carrée) qui ne prend qu'un seul opérande.
# 3. L'opération MAX (valeur maximale). 
#
# Règle importante pour MAX : 
# Avec la Notation Polonaise Inverse, nous devons avoir un nombre fixe d'opérandes 
# par opérateur pour éviter l'utilisation de parenthèses. Pour ce kata, l'opérateur 
# MAX prendra TOUJOURS exactement 2 opérandes. 
# 
# Exemples :
# - "4 5 MAX 1 2 MAX *" est valide. (Évalué comme max(4,5) * max(1,2) = 5 * 2 = 10)
# - "5 3 4 2 9 1 MAX" n'est PAS une expression valide selon cette règle fixe.
# ==============================================================================


def evaluate_rpn(expression: str) -> float:
    """
    Évalue une expression mathématique en Notation Polonaise Inverse (NPI).
    """
    if not expression.strip():
        return 0.0

    stack = []
    tokens = expression.split()

    for token in tokens:
        # Gestion des opérateurs à 2 opérandes
        if token in ("+", "-", "*", "/", "MAX"):
            if len(stack) < 2:
                raise ValueError(f"Pas assez d'opérandes pour l'opérateur {token}")
            
            # Attention à l'ordre : le dernier empilé est l'opérande de droite
            right = stack.pop()
            left = stack.pop()
            
            if token == "+":
                stack.append(left + right)
            elif token == "-":
                stack.append(left - right)
            elif token == "*":
                stack.append(left * right)
            elif token == "/":
                if right == 0:
                    raise ZeroDivisionError("Division par zéro")
                stack.append(left / right)
            elif token == "MAX":
                stack.append(max(left, right))
                
        # Gestion des opérateurs à 1 opérande
        elif token == "SQRT":
            if len(stack) < 1:
                raise ValueError("Pas assez d'opérandes pour l'opérateur SQRT")
            
            val = stack.pop()
            if val < 0:
                raise ValueError("Racine carrée d'un nombre négatif")
            stack.append(math.sqrt(val))
            
        # Si c'est un nombre
        else:
            try:
                stack.append(float(token))
            except ValueError:
                raise ValueError(f"Token invalide : {token}")

    # À la fin de l'évaluation, il ne doit rester qu'un seul élément dans la pile
    if len(stack) != 1:
        raise ValueError("L'expression est invalide, il reste des opérandes non utilisés")

    return stack[0]


# ==============================================================================
# TESTS UNITAIRES
# ==============================================================================

class TestRPNCalculator(unittest.TestCase):
    
    def test_empty_expression(self):
        self.assertEqual(evaluate_rpn(""), 0.0)
        
    def test_single_number(self):
        self.assertEqual(evaluate_rpn("42"), 42.0)
        self.assertEqual(evaluate_rpn("3.14"), 3.14)
        
    def test_basic_arithmetic(self):
        self.assertEqual(evaluate_rpn("3 4 +"), 7.0)
        self.assertEqual(evaluate_rpn("10 4 -"), 6.0)
        self.assertEqual(evaluate_rpn("3 4 *"), 12.0)
        self.assertEqual(evaluate_rpn("12 4 /"), 3.0)
        
    def test_complex_expression(self):
        # (3 + 4) * 5 = 35
        self.assertEqual(evaluate_rpn("3 4 + 5 *"), 35.0)
        # 5 * (3 + 4) = 35
        self.assertEqual(evaluate_rpn("5 3 4 + *"), 35.0)
        
    def test_sqrt_operator(self):
        self.assertEqual(evaluate_rpn("9 SQRT"), 3.0)
        self.assertEqual(evaluate_rpn("16 SQRT 2 *"), 8.0)
        
    def test_max_operator(self):
        self.assertEqual(evaluate_rpn("4 5 MAX"), 5.0)
        self.assertEqual(evaluate_rpn("10 2 MAX"), 10.0)
        
    def test_rpn_kata_example(self):
        # Exemple de l'énoncé : "4 5 MAX 1 2 MAX *"
        self.assertEqual(evaluate_rpn("4 5 MAX 1 2 MAX *"), 10.0)
        
    def test_errors(self):
        with self.assertRaises(ValueError):
            evaluate_rpn("3 +") # Pas assez d'opérandes
            
        with self.assertRaises(ValueError):
            evaluate_rpn("3 4 5 +") # Trop d'opérandes à la fin
            
        with self.assertRaises(ZeroDivisionError):
            evaluate_rpn("4 0 /")
            
        with self.assertRaises(ValueError):
            evaluate_rpn("-4 SQRT")
            
        with self.assertRaises(ValueError):
            evaluate_rpn("FOO 4 +") # Token invalide

if __name__ == '__main__':
    unittest.main()