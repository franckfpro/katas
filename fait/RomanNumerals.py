"""
================================================================================
KATA : Les Chiffres Romains (Roman Numerals)
================================================================================

DESCRIPTION DU PROBLÈME :
Les Romains écrivaient les nombres en utilisant des lettres : I, V, X, L, C, D, M.
Il n'est pas nécessaire de gérer les nombres supérieurs à 3000.

PARTIE I :
Écrire une fonction qui convertit un nombre entier "normal" en sa représentation
en chiffres romains.
Exemples :
    1  --> I
    10 --> X
    7  --> VII

PARTIE II :
Écrire une fonction qui fait l'inverse : convertir une chaîne de caractères
représentant un chiffre romain en un nombre entier.

INDICES POUR LE CODE :
- Pouvez-vous rendre le code particulièrement beau et lisible ?
- Quelle est la meilleure structure de données pour stocker les correspondances ?
================================================================================
"""

import pytest

roman2arabic = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
arabic2roman = {
    1: "I",
    4: "IV",
    5: "V",
    9: "IX",
    10: "X",
    40: "XL",
    50: "L",
    90: "XC",
    100: "C",
    400: "CD",
    500: "D",
    900: "CM",
    1000: "M",
}
# c'est de la triche de mettre les codes des types 4, ce serait plus interressant de passer par une vérification de 4 chaines identiques à la suite
# arabic2roman = {1: "I", 5: "V", 10: "X", 50: "L", 100: "C", 500: "D", 1000: "M"}


def to_roman(number: int) -> str:
    if number <= 0 or number > 3000:
        raise ValueError
    result = ""
    for key in sorted(arabic2roman.keys(), reverse=True):
        while number >= key:
            result += arabic2roman[key]
            number -= key

    return result


def from_roman(roman_str: str) -> int:
    result = 0
    for i in range(len(roman_str) - 1):
        if roman_str[i] not in roman2arabic or roman_str[-1] not in roman2arabic:
            raise ValueError
        if roman2arabic[roman_str[i]] < roman2arabic[roman_str[i + 1]]:
            result -= roman2arabic[roman_str[i]]
        else:
            result += roman2arabic[roman_str[i]]
    result += roman2arabic[roman_str[-1]]
    return result


# ------------------------------------------------------------------------------
# TESTS UNITAIRES (pytest)
# ------------------------------------------------------------------------------

# Liste de cas de test (Arabe, Romain) partagée pour valider les deux sens
TEST_CASES = [
    (1, "I"),
    (3, "III"),
    (4, "IV"),
    (5, "V"),
    (6, "VI"),
    (9, "IX"),
    (10, "X"),
    (27, "XXVII"),
    (48, "XLVIII"),
    (50, "L"),
    (90, "XC"),
    (141, "CXLI"),
    (400, "CD"),
    (500, "D"),
    (900, "CM"),
    (1000, "M"),
    (1984, "MCMLXXXIV"),
    (3000, "MMM"),
]


@pytest.mark.parametrize("arabic, expected_roman", TEST_CASES)
def test_should_convert_arabic_to_roman(arabic, expected_roman):
    """Vérifie la conversion des entiers vers les chiffres romains (Partie I)."""
    assert to_roman(arabic) == expected_roman


@pytest.mark.parametrize("expected_arabic, roman", TEST_CASES)
def test_should_convert_roman_to_arabic(expected_arabic, roman):
    """Vérifie la conversion des chiffres romains vers les entiers (Partie II)."""
    assert from_roman(roman) == expected_arabic


def test_to_roman_boundaries_and_errors():
    """Vérifie que la fonction to_roman lève des exceptions pour les entrées hors limites."""
    with pytest.raises(ValueError):
        to_roman(0)
    with pytest.raises(ValueError):
        to_roman(3001)


def test_from_roman_invalid_characters():
    """Vérifie que la fonction from_roman lève une exception sur un caractère inconnu."""
    with pytest.raises(ValueError):
        from_roman("MCXG")
