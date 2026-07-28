"""
Kata Mathematical AST - Consignes

Origine :
Ce kata a été initialement écrit pour implémenter le patron de conception Visiteur (Visitor pattern).

Objectifs :

Étape 1 :
Écrire un programme qui construit un Arbre Syntaxique Abstrait (AST) d'une expression
mathématique en Notation Polonaise Inverse (RPN) à partir d'une chaîne de caractères (ex: "3 4 +").
Vous devez concevoir les objets ou structures de données qui composeront votre AST.

Étape 2 :
Créer des méthodes ou fonctions permettant de :
- Reconstruire la représentation RPN à partir de l'AST.
- Construire la représentation infixe (classique) à partir de l'AST.
- Évaluer mathématiquement l'AST pour obtenir le résultat.

Étape 3 :
Construire la représentation infixe avec le strict minimum de parenthèses.
(ex: "3 * (4 + 5)" au lieu de "(3 * (4 + 5))").

Étape 4 :
Implémenter les opérations avancées :
- Exposant (^)
- Flèche de Knuth (↑) - Note : Pour simplifier, nous la traiterons comme une itération 
  d'exposant ou simplement comme synonyme d'exposant classique dans ce contexte.
"""

import unittest
import math

class ASTNode:
    """Classe de base pour un nœud de l'Arbre Syntaxique Abstrait."""
    def evaluate(self):
        raise NotImplementedError
    def to_rpn(self):
        raise NotImplementedError
    def to_infix(self):
        raise NotImplementedError
    def precedence(self):
        return 99  # Priorité maximale par défaut


class NumberNode(ASTNode):
    """Représente une valeur numérique dans l'AST."""
    def __init__(self, value):
        self.value = float(value)

    def evaluate(self):
        return self.value

    def to_rpn(self):
        # Formatage pour enlever le .0 si c'est un entier
        return str(int(self.value)) if self.value.is_integer() else str(self.value)

    def to_infix(self):
        return self.to_rpn()


class OperationNode(ASTNode):
    """Représente une opération binaire dans l'AST."""
    
    # Dictionnaire des opérations supportées et de leur priorité
    OPERATIONS = {
        '+': (1, lambda a, b: a + b),
        '-': (1, lambda a, b: a - b),
        '*': (2, lambda a, b: a * b),
        '/': (2, lambda a, b: a / b),
        '^': (3, lambda a, b: a ** b),
        '↑': (3, lambda a, b: a ** b), # Simplification de la flèche de Knuth
    }

    # Opérateurs associatifs à droite
    RIGHT_ASSOCIATIVE = ['^', '↑']

    def __init__(self, left: ASTNode, right: ASTNode, operator: str):
        self.left = left
        self.right = right
        self.operator = operator

    def precedence(self):
        return self.OPERATIONS[self.operator][0]

    def evaluate(self):
        func = self.OPERATIONS[self.operator][1]
        return func(self.left.evaluate(), self.right.evaluate())

    def to_rpn(self):
        return f"{self.left.to_rpn()} {self.right.to_rpn()} {self.operator}"

    def to_infix(self):
        left_str = self.left.to_infix()
        right_str = self.right.to_infix()

        # Règle pour le minimum de parenthèses (Étape 3)
        # Si le nœud enfant a une priorité inférieure, on l'entoure de parenthèses.
        if isinstance(self.left, OperationNode):
            if self.left.precedence() < self.precedence():
                left_str = f"({left_str})"
            # Cas spécial : associativité à droite (ex: 2^(3^4))
            elif self.left.precedence() == self.precedence() and self.operator in self.RIGHT_ASSOCIATIVE:
                 left_str = f"({left_str})"

        if isinstance(self.right, OperationNode):
            if self.right.precedence() < self.precedence():
                right_str = f"({right_str})"
            # Cas spécial : associativité à gauche (ex: 10 - (5 - 2))
            elif self.right.precedence() == self.precedence() and self.operator not in self.RIGHT_ASSOCIATIVE:
                right_str = f"({right_str})"

        return f"{left_str} {self.operator} {right_str}"


def parse_rpn(expression: str) -> ASTNode:
    """
    Construit un AST à partir d'une chaîne RPN (Étape 1).
    """
    stack = []
    tokens = expression.split()

    for token in tokens:
        if token in OperationNode.OPERATIONS:
            # Dépile les deux derniers éléments (le premier sorti est le terme de droite)
            right = stack.pop()
            left = stack.pop()
            stack.append(OperationNode(left, right, token))
        else:
            # Si c'est un nombre, on l'empile
            stack.append(NumberNode(token))
            
    return stack[0]


# ==========================================
# SUITE DE TESTS UNITAIRES
# ==========================================

class TestMathematicalAST(unittest.TestCase):

    def test_step1_and_2_basic_ast_evaluation_and_rpn(self):
        ast = parse_rpn("3 4 +")
        self.assertEqual(ast.evaluate(), 7.0)
        self.assertEqual(ast.to_rpn(), "3 4 +")
        self.assertEqual(ast.to_infix(), "3 + 4")

        ast2 = parse_rpn("10 4 3 + *")
        self.assertEqual(ast2.evaluate(), 70.0)
        self.assertEqual(ast2.to_rpn(), "10 4 3 + *")

    def test_step3_minimum_parenthesis(self):
        # 10 * (4 + 3) -> L'addition doit avoir des parenthèses car * est prioritaire
        ast1 = parse_rpn("10 4 3 + *")
        self.assertEqual(ast1.to_infix(), "10 * (4 + 3)")

        # (10 * 4) + 3 -> La multiplication n'a pas besoin de parenthèses
        ast2 = parse_rpn("10 4 * 3 +")
        self.assertEqual(ast2.to_infix(), "10 * 4 + 3")

        # 10 - (5 - 2) -> Associativité à gauche, la soustraction de droite a besoin de parenthèses
        ast3 = parse_rpn("10 5 2 - -")
        self.assertEqual(ast3.to_infix(), "10 - (5 - 2)")

        # (10 - 5) - 2 -> Pas besoin de parenthèses
        ast4 = parse_rpn("10 5 - 2 -")
        self.assertEqual(ast4.to_infix(), "10 - 5 - 2")

    def test_step4_advanced_operators(self):
        # Test Exposant : 2 ^ 3 = 8
        ast_exp = parse_rpn("2 3 ^")
        self.assertEqual(ast_exp.evaluate(), 8.0)
        self.assertEqual(ast_exp.to_infix(), "2 ^ 3")

        # Test Flèche de Knuth : 3 ↑ 3 = 27
        ast_knuth = parse_rpn("3 3 ↑")
        self.assertEqual(ast_knuth.evaluate(), 27.0)
        
        # Test associativité à droite pour l'exposant : 2 ^ (3 ^ 2)
        ast_right_assoc = parse_rpn("2 3 2 ^ ^")
        self.assertEqual(ast_right_assoc.to_infix(), "2 ^ (3 ^ 2)")
        self.assertEqual(ast_right_assoc.evaluate(), 512.0)

if __name__ == '__main__':
    unittest.main()