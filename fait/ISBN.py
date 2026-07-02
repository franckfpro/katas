#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
KATA : Validation ISBN (International Standard Book Number)
===========================================================

Il existe deux normes ISBN : ISBN-10 et ISBN-13. 
Le support de l'ISBN-13 est essentiel, tandis que le support de l'ISBN-10 est optionnel (mais inclus ici).

Exemples valides :
-----------------
ISBN-13:    9780470059029
            978 0 471 48648 0
            978-0596809485
            978-0-13-149505-0
            978-0-262-13472-9

ISBN-10:    0471958697
            0 471 60695 2
            0-470-84525-2
            0-321-14653-0

Détails techniques :
-------------------
L'ISBN-10 est composé de 9 chiffres plus un chiffre de contrôle (qui peut être 'X').
L'ISBN-13 est composé de 12 chiffres plus un chiffre de contrôle.
Les espaces et les tirets peuvent être inclus mais ne sont pas significatifs.

Calcul de la clé de contrôle ISBN-13 :
Multiplication de chaque chiffre alternativement par 1 ou 3 (1x1er, 3x2e, 1x3e, etc.).
Somme de ces produits, reste de la division par 10 (modulo 10), puis soustraction de ce résultat à 10.
Si le résultat final est 10, la clé est 0.

Calcul de la clé de contrôle ISBN-10 :
Multiplication de chaque chiffre par sa position (1x1er, 2x2e, ..., 10x10e).
La somme de ces produits doit être un multiple de 11 (modulo 11 == 0). 
Le caractère 'X' est utilisé pour représenter la valeur 10.

Objectif :
----------
Créer une fonction qui prend une chaîne de caractères et renvoie True si elle 
représente un ISBN-13 ou un ISBN-10 valide, et False sinon.
"""

import unittest


def is_valid_isbn(isbn_str: str) -> bool:
    """
    Vérifie si une chaîne de caractères est un ISBN-10 ou ISBN-13 valide.
    """
    isbn_str_clean = []
    for carac in isbn_str:
        if carac.isdigit():
            isbn_str_clean.append(carac)
    if len(isbn_str_clean) == 10:
        calcul_controle_10 = 0
        for i, num in enumerate(isbn_str_clean):
            calcul_controle_10 += int(num) * (i+1)
        if calcul_controle_10 % 11 == 0:
            return True
        else:
            return False
    calcul_controle = 0
    for i, num in enumerate(isbn_str_clean[:-1]):
        if i % 2 == 0:
            calcul_controle += int(num)
        else:
            calcul_controle += int(num) * 3
    calcul_controle_modulo = calcul_controle % 10
    if calcul_controle_modulo != 0:
        calcul_controle_modulo -= 10
    if abs(calcul_controle_modulo) == int(isbn_str_clean[-1]):
        return True
    return False

# solution bis

def is_valid_isbn(isbn_str: str) -> bool:
    """
    Vérifie si une chaîne de caractères est un ISBN-10 ou ISBN-13 valide.
    """
    # Nettoyage de la chaîne : on retire les espaces et les tirets
    cleaned = isbn_str.replace(" ", "").replace("-", "")
    
    # --- Validation ISBN-13 ---
    if len(cleaned) == 13 and cleaned.isdigit():
        digits = [int(char) for char in cleaned]
        total = 0
        for i in range(12):
            weight = 1 if i % 2 == 0 else 3
            total += digits[i] * weight
        
        check_digit = (10 - (total % 10)) % 10
        return digits[12] == check_digit

    # --- Validation ISBN-10 ---
    elif len(cleaned) == 10:
        # Les 9 premiers caractères doivent être des chiffres
        if not cleaned[:9].isdigit():
            return False
        
        # Le dernier caractère peut être un chiffre ou 'X'
        last_char = cleaned[9].upper()
        if not (last_char.isdigit() or last_char == 'X'):
            return False
        
        # Calcul de la somme pondérée
        total = 0
        for i in range(9):
            total += int(cleaned[i]) * (i + 1)
        
        # Gestion du cas particulier 'X'
        last_value = 10 if last_char == 'X' else int(last_char)
        total += last_value * 10
        
        return total % 11 == 0

    return False


# ==============================================================================
# TESTS UNITAIRES
# ==============================================================================

class TestIsbnValidator(unittest.TestCase):

    def test_valid_isbn13(self):
        """Test des formats ISBN-13 valides (avec ou sans séparateurs)."""
        valid_examples = [
            "9780470059029",
            "978 0 471 48648 0",
            "978-0596809485",
            "978-0-13-149505-0",
            "978-0-262-13472-9"
        ]
        for isbn in valid_examples:
            with self.subTest(isbn=isbn):
                self.assertTrue(is_valid_isbn(isbn))

    def test_invalid_isbn13(self):
        """Test des formats ISBN-13 invalides."""
        invalid_examples = [
            "9780470059028",  # Mauvaise clé de contrôle
            "978-0-13-149505-01",  # Trop long
            "978-0-13-14950-A"  # Lettre interdite
        ]
        for isbn in invalid_examples:
            with self.subTest(isbn=isbn):
                self.assertFalse(is_valid_isbn(isbn))

    def test_valid_isbn10(self):
        """Test des formats ISBN-10 valides (avec ou sans séparateurs, incluant 'X')."""
        valid_examples = [
            "0471958697",
            "0 471 60695 2",
            "0-470-84525-2",
            "0-321-14653-0",
            "0-13-149505-X"  # Clé de contrôle avec 'X'
        ]
        for isbn in valid_examples:
            with self.subTest(isbn=isbn):
                self.assertTrue(is_valid_isbn(isbn))

    def test_invalid_isbn10(self):
        """Test des formats ISBN-10 invalides."""
        invalid_examples = [
            "0471958698",  # Mauvaise clé de contrôle
            "0-321-14653-X",  # Mauvaise clé de contrôle ('X' au lieu de chiffre)
            "047195869",  # Trop court
            "047A958697"  # Lettre au milieu
        ]
        for isbn in invalid_examples:
            with self.subTest(isbn=isbn):
                self.assertFalse(is_valid_isbn(isbn))


if __name__ == "__main__":
    unittest.main()
