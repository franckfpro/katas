import unittest

# ==============================================================================
# CONSIGNES DU KATA (Traduites en Français)
# ==============================================================================
"""
À propos de ce Kata :
Vous devez implémenter une fonction `compute(number: str) -> str` qui respecte 
les règles métier suivantes.

Étape 1 - Les Règles :
  - Si le nombre est divisible par 3, écrivez "Foo"
  - Si le nombre est divisible par 5, ajoutez "Bar"
  - Si le nombre est divisible par 7, ajoutez "Qix"
  - Pour chaque chiffre 3, 5, 7, ajoutez "Foo", "Bar", "Qix" dans l'ordre 
    d'apparition des chiffres.

Exemples Étape 1 :
  1  => 1
  2  => 2
  3  => FooFoo (divisible par 3, contient 3)
  4  => 4
  5  => BarBar (divisible par 5, contient 5)
  6  => Foo (divisible par 3)
  7  => QixQix (divisible par 7, contient 7)
  8  => 8
  9  => Foo
  13 => Foo
  15 => FooBarBar (divisible par 3, divisible par 5, contient 5)
  21 => FooQix
  33 => FooFooFoo (divisible par 3, contient deux 3)
  51 => FooBar
  53 => BarFoo

Étape 2 - Nouvelle demande métier :
  - Nous devons garder une trace des zéros. Chaque '0' doit être remplacé 
    par le caractère '*'.

Exemples Étape 2 :
  101   => 1*1
  303   => FooFoo*Foo
  105   => FooBarQix*Bar
  10101 => FooQix**
"""

# ==============================================================================
# VOTRE IMPLEMENTATION (Le Kata à résoudre)
# ==============================================================================

def compute(number: str) -> str:
    """
    Transforme un nombre en chaîne de caractères selon les règles de FooBarQix.
    """
    num = int(number)
    result = ""

    # 1. Règles de divisibilité
    if num % 3 == 0:
        result += "Foo"
    if num % 5 == 0:
        result += "Bar"
    if num % 7 == 0:
        result += "Qix"

    # 2. Règles d'occurrence des chiffres
    for digit in number:
        if digit == '3':
            result += "Foo"
        elif digit == '5':
            result += "Bar"
        elif digit == '7':
            result += "Qix"
        elif digit == '0':
            result += "*"  # Règle de l'étape 2

    # 3. Traitement final : si aucun Foo, Bar, ou Qix n'a été ajouté
    # On vérifie cela en retirant temporairement les étoiles.
    if not result.replace('*', ''):
        # On retourne le nombre d'origine en remplaçant juste les '0' par '*'
        return number.replace('0', '*')

    return result


# ==============================================================================
# TESTS UNITAIRES (Validation du comportement)
# ==============================================================================

class TestFooBarQix(unittest.TestCase):

    def test_should_return_number_when_no_rules_apply(self):
        self.assertEqual(compute("1"), "1")
        self.assertEqual(compute("2"), "2")
        self.assertEqual(compute("4"), "4")
        self.assertEqual(compute("8"), "8")

    def test_should_apply_divisibility_rules_only(self):
        self.assertEqual(compute("6"), "Foo")

    def test_should_apply_occurrence_rules_only(self):
        self.assertEqual(compute("13"), "Foo")
        self.assertEqual(compute("53"), "BarFoo")

    def test_should_apply_divisibility_and_occurrence_rules(self):
        self.assertEqual(compute("3"), "FooFoo")
        self.assertEqual(compute("5"), "BarBar")
        self.assertEqual(compute("7"), "QixQix")
        self.assertEqual(compute("15"), "FooBarBar")
        self.assertEqual(compute("21"), "FooQix")
        self.assertEqual(compute("33"), "FooFooFoo")
        self.assertEqual(compute("51"), "FooBar")

    def test_step_2_should_replace_zeros_with_stars_when_no_other_rules_apply(self):
        self.assertEqual(compute("101"), "1*1")

    def test_step_2_should_include_stars_with_foo_bar_qix(self):
        self.assertEqual(compute("303"), "FooFoo*Foo")
        self.assertEqual(compute("105"), "FooBarQix*Bar")
        self.assertEqual(compute("10101"), "FooQix**")
        self.assertEqual(compute("10"), "Bar*") # Divisible par 5, contient un 0

if __name__ == '__main__':
    unittest.main()