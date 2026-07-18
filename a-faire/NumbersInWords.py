"""
Kata Numbers in Words (Nombres en lettres) - Consignes

Contexte :
Il arrive parfois dans la vie réelle que l'on doive écrire des montants en toutes lettres. 
Par exemple, pour éviter les fraudes et les erreurs sur les chèques ou les contrats, 
la loi exige souvent d'écrire le montant en chiffres ET en lettres. 
Si vous voulez transférer 745 $, vous devez remplir deux champs :
- 745 (montant en chiffres)
- seven hundred forty five (montant en lettres)

Objectifs :
- Étape 1 : Écrire une fonction pour convertir des nombres entiers en mots.
- Étape 2 : Écrire une fonction pour faire l'inverse (convertir les mots en nombres).
- Étape 3 : Faire tout cela en utilisant le Développement Dirigé par les Tests (TDD).
"""

import unittest

# Dictionnaires de correspondance pour la conversion
NUMBERS_TO_WORDS = {
    0: "zero", 1: "one", 2: "two", 3: "three", 4: "four",
    5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
    10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen",
    15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen",
    20: "twenty", 30: "thirty", 40: "forty", 50: "fifty",
    60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety"
}

SCALES = ["", "thousand", "million", "billion"]

# Dictionnaire inversé pour l'étape 2
WORDS_TO_NUMBERS = {word: num for num, word in NUMBERS_TO_WORDS.items()}
WORDS_TO_NUMBERS.update({"hundred": 100, "thousand": 1000, "million": 1000000, "billion": 1000000000})


def number_to_words(n: int) -> str:
    """Étape 1 : Convertit un nombre entier en mots (anglais)."""
    if n == 0:
        return NUMBERS_TO_WORDS[0]

    def process_chunk(number: int) -> list:
        """Traite un bloc de 3 chiffres (ex: 745 -> seven hundred forty five)."""
        chunk_words = []
        hundreds = number // 100
        remainder = number % 100

        if hundreds > 0:
            chunk_words.append(NUMBERS_TO_WORDS[hundreds])
            chunk_words.append("hundred")

        if remainder > 0:
            if remainder in NUMBERS_TO_WORDS:
                chunk_words.append(NUMBERS_TO_WORDS[remainder])
            else:
                tens = (remainder // 10) * 10
                units = remainder % 10
                chunk_words.append(NUMBERS_TO_WORDS[tens])
                chunk_words.append(NUMBERS_TO_WORDS[units])
                
        return chunk_words

    words = []
    scale_idx = 0

    while n > 0:
        chunk = n % 1000
        if chunk > 0:
            chunk_words = process_chunk(chunk)
            if SCALES[scale_idx]:
                chunk_words.append(SCALES[scale_idx])
            words = chunk_words + words
        
        n //= 1000
        scale_idx += 1

    return " ".join(words)


def words_to_number(words_str: str) -> int:
    """Étape 2 : Convertit une chaîne de mots (anglais) en nombre entier."""
    if words_str.strip().lower() == "zero":
        return 0

    result = 0
    current_chunk = 0
    
    # Nettoyage de la chaîne (gestion des tirets optionnels et des "and")
    clean_words = words_str.lower().replace("-", " ").replace(" and ", " ").split()

    for word in clean_words:
        if word not in WORDS_TO_NUMBERS:
            continue
            
        value = WORDS_TO_NUMBERS[word]

        if value == 100:
            current_chunk *= value
        elif value >= 1000:
            current_chunk *= value
            result += current_chunk
            current_chunk = 0
        else:
            current_chunk += value

    return result + current_chunk


# ==========================================
# SUITE DE TESTS UNITAIRES
# ==========================================

class TestNumbersInWords(unittest.TestCase):

    def test_step1_number_to_words_single_digits(self):
        self.assertEqual(number_to_words(0), "zero")
        self.assertEqual(number_to_words(7), "seven")

    def test_step1_number_to_words_tens_and_teens(self):
        self.assertEqual(number_to_words(15), "fifteen")
        self.assertEqual(number_to_words(42), "forty two")

    def test_step1_number_to_words_hundreds(self):
        self.assertEqual(number_to_words(745), "seven hundred forty five")

    def test_step1_number_to_words_large_numbers(self):
        self.assertEqual(number_to_words(1999), "one thousand nine hundred ninety nine")
        self.assertEqual(number_to_words(3000200), "three million two hundred")

    def test_step2_words_to_number_simple(self):
        self.assertEqual(words_to_number("zero"), 0)
        self.assertEqual(words_to_number("seven"), 7)
        self.assertEqual(words_to_number("forty two"), 42)
        # Tolérance pour les tirets et les "and"
        self.assertEqual(words_to_number("forty-two"), 42) 

    def test_step2_words_to_number_complex(self):
        self.assertEqual(words_to_number("seven hundred forty five"), 745)
        self.assertEqual(words_to_number("seven hundred and forty five"), 745)
        self.assertEqual(words_to_number("one thousand nine hundred ninety nine"), 1999)
        self.assertEqual(words_to_number("three million two hundred"), 3000200)

    def test_round_trip_conversion(self):
        """Vérifie que la conversion dans les deux sens retombe sur la valeur initiale."""
        original_number = 123456789
        words = number_to_words(original_number)
        self.assertEqual(words_to_number(words), original_number)


if __name__ == '__main__':
    unittest.main()