import unittest

# ==============================================================================
# KATA : CALCULATRICE ROMAINE (ROMAN CALCULATOR)
# ==============================================================================
#
# CONSIGNES :
# "En tant que comptable romain, je veux additionner des chiffres romains parce 
# que le faire manuellement est trop fastidieux."
#
# Étant donné les chiffres romains (I, V, X, L, C, D, M qui signifient 
# respectivement un, cinq, dix, cinquante, cent, cinq cents et mille), 
# créez deux nombres et additionnez-les. 
#
# Puisque nous sommes dans la Rome antique, les décimales ou les entiers (int) 
# n'existent pas, nous devons faire cela en manipulant directement les chaînes 
# de caractères.
#
# Exemple : "XIV" + "LX" = "LXXIV"
#
# RÈGLES D'UN NOMBRE ROMAIN :
# 1. Les chiffres peuvent être concaténés pour former un chiffre plus grand 
#    ("XX" + "II" = "XXII").
# 2. Si un petit chiffre est placé avant un plus grand, cela signifie une 
#    soustraction du plus petit au plus grand ("IV" = 4, "CM" = 900).
# 3. Pour les chiffres I, X ou C, vous ne pouvez pas en avoir plus de trois 
#    ("II" + "II" = "IV").
# 4. Pour les chiffres V, L ou D, vous ne pouvez pas en avoir plus d'un 
#    ("D" + "D" = "M").
#
# INDICE :
# Le regroupement de chaînes et la concaténation sont la clé pour résoudre ce 
# kata. N'oubliez pas la règle selon laquelle les chiffres inférieurs peuvent 
# précéder les chiffres supérieurs.
# ==============================================================================


def add_roman_numerals(roman1: str, roman2: str) -> str:
    """
    Additionne deux nombres romains en utilisant uniquement 
    la manipulation de chaînes de caractères.
    """
    # Étape 1 : Remplacer la notation soustractive par de l'addition pure
    expand_map = {
        "CM": "DCCCC",
        "CD": "CCCC",
        "XC": "LXXXX",
        "XL": "XXXX",
        "IX": "VIIII",
        "IV": "IIII"
    }
    for sub, add in expand_map.items():
        roman1 = roman1.replace(sub, add)
        roman2 = roman2.replace(sub, add)

    # Étape 2 : Concaténer les deux chaînes
    combined = roman1 + roman2

    # Étape 3 : Trier les symboles du plus grand au plus petit
    # L'ordre d'importance des symboles romains
    order = {"M": 1, "D": 2, "C": 3, "L": 4, "X": 5, "V": 6, "I": 7}
    combined = "".join(sorted(combined, key=lambda x: order[x]))

    # Étape 4 : Simplifier et regrouper (en cascade, du plus petit au plus grand)
    simplify_map = {
        "IIIII": "V",
        "VV": "X",
        "XXXXX": "L",
        "LL": "C",
        "CCCCC": "D",
        "DD": "M"
    }
    # En appliquant ces remplacements de manière séquentielle, 
    # les nouveaux symboles créés sont capturés par les remplacements suivants.
    for repeated, simplified in simplify_map.items():
        combined = combined.replace(repeated, simplified)

    # Étape 5 : Remettre la notation soustractive (compacter)
    compact_map = {
        "DCCCC": "CM",
        "CCCC": "CD",
        "LXXXX": "XC",
        "XXXX": "XL",
        "VIIII": "IX",
        "IIII": "IV"
    }
    for add, sub in compact_map.items():
        combined = combined.replace(add, sub)

    return combined


# ==============================================================================
# TESTS UNITAIRES
# ==============================================================================

class TestRomanCalculator(unittest.TestCase):
    
    def test_simple_concatenation(self):
        self.assertEqual(add_roman_numerals("XX", "II"), "XXII")
        self.assertEqual(add_roman_numerals("I", "I"), "II")
        
    def test_simplification_grouping(self):
        self.assertEqual(add_roman_numerals("II", "II"), "IV")
        self.assertEqual(add_roman_numerals("D", "D"), "M")
        self.assertEqual(add_roman_numerals("V", "V"), "X")
        
    def test_subtractive_notation_handling(self):
        self.assertEqual(add_roman_numerals("XIV", "LX"), "LXXIV")
        self.assertEqual(add_roman_numerals("IV", "IV"), "VIII")
        self.assertEqual(add_roman_numerals("IX", "IX"), "XVIII")
        self.assertEqual(add_roman_numerals("CM", "CM"), "MDCCC")
        
    def test_cascading_simplification(self):
        # 1994 (MCMXCIV) + 6 (VI) = 2000 (MM)
        self.assertEqual(add_roman_numerals("MCMXCIV", "VI"), "MM")
        # 49 (XLIX) + 2 (II) = 51 (LI)
        self.assertEqual(add_roman_numerals("XLIX", "II"), "LI")
        # 399 (CCCXCIX) + 1 (I) = 400 (CD)
        self.assertEqual(add_roman_numerals("CCCXCIX", "I"), "CD")

if __name__ == '__main__':
    unittest.main()