import unittest

# =============================================================================
# CONSIGNES DU KATA : RANGE (INTERVALLES)
# =============================================================================
# Le type "Range" (Intervalle) pose de nombreux petits défis intéressants.
# L'objectif est d'implémenter une classe représentant un intervalle d'entiers
# et capable de répondre aux règles suivantes :
#
# 1. Contient (Contains) :
#    - L'intervalle entier [2,6) contient {2,4}
#    - L'intervalle [2,6) ne contient pas {-1,1,6,10}
#
# 2. Tous les points (getAllPoints) :
#    - Pour [2,6), tous les points = {2,3,4,5}
#
# 3. Contient un intervalle (ContainsRange) :
#    - [2,5) ne contient pas [7,10)
#    - [2,5) ne contient pas [3,10)
#    - [3,5) ne contient pas [2,10)
#    - [2,10) contient [3,5]
#    - [3,5] contient [3,5)
#
# 4. Points aux extrémités (endPoints) :
#    - Pour [2,6), les extrémités = {2,5}
#    - Pour [2,6], les extrémités = {2,6}
#    - Pour (2,6), les extrémités = {3,5}
#    - Pour (2,6], les extrémités = {3,6}
#
# 5. Chevauchement (overlapsRange) :
#    - [2,5) ne chevauche pas [7,10)
#    - [2,10) chevauche [3,5)
#    - [3,5) chevauche [3,5)
#    - [2,5) chevauche [3,10)
#    - [3,5) chevauche [2,10)
#
# 6. Égalité (Equals) :
#    - [3,5) est égal à [3,5)
#    - [2,10) n'est pas égal à [3,5)
#    - [2,5) n'est pas égal à [3,10)
#    - [3,5) n'est pas égal à [2,10)
# =============================================================================

class IntegerRange:
    def __init__(self, range_str: str):
        """
        Initialise un intervalle à partir d'une chaîne comme "[2,6)" ou "(2,6]".
        '[' ou ']' = inclusif
        '(' ou ')' = exclusif
        """
        self.range_str = range_str.strip()
        
        # Vérification des caractères d'inclusion/exclusion
        self.start_inclusive = self.range_str[0] == '['
        self.end_inclusive = self.range_str[-1] == ']'
        
        # Extraction des valeurs numériques
        inner_parts = self.range_str[1:-1].split(',')
        if len(inner_parts) != 2:
            raise ValueError("Le format de l'intervalle doit être [a,b)")
            
        self.raw_start = int(inner_parts[0].strip())
        self.raw_end = int(inner_parts[1].strip())

    def get_all_points(self) -> set:
        """Retourne l'ensemble de tous les entiers contenus dans l'intervalle."""
        start = self.raw_start if self.start_inclusive else self.raw_start + 1
        end = self.raw_end if self.end_inclusive else self.raw_end - 1
        # range() en Python est exclusif sur la fin, donc on ajoute 1
        return set(range(start, end + 1))

    def contains(self, values: set) -> bool:
        """Vérifie si toutes les valeurs fournies sont dans l'intervalle."""
        points = self.get_all_points()
        return all(v in points for v in values)

    def contains_range(self, other: 'IntegerRange') -> bool:
        """Vérifie si un autre intervalle est totalement inclus dans celui-ci."""
        return other.get_all_points().issubset(self.get_all_points())

    def end_points(self) -> set:
        """Retourne les extrémités réelles (min et max inclus) de l'intervalle."""
        points = self.get_all_points()
        if not points:
            return set()
        return {min(points), max(points)}

    def overlaps_range(self, other: 'IntegerRange') -> bool:
        """Vérifie si cet intervalle chevauche un autre intervalle."""
        return not self.get_all_points().isdisjoint(other.get_all_points())

    def __eq__(self, other: object) -> bool:
        """Vérifie l'égalité logique (les points contenus) entre deux intervalles."""
        if not isinstance(other, IntegerRange):
            return False
        return self.get_all_points() == other.get_all_points()

    def __repr__(self) -> str:
        return f"IntegerRange('{self.range_str}')"


# =============================================================================
# TESTS UNITAIRES
# =============================================================================
class TestIntegerRange(unittest.TestCase):

    def test_contains(self):
        r = IntegerRange("[2,6)")
        self.assertTrue(r.contains({2, 4}))
        self.assertFalse(r.contains({-1, 1, 6, 10}))

    def test_get_all_points(self):
        r = IntegerRange("[2,6)")
        self.assertEqual(r.get_all_points(), {2, 3, 4, 5})

    def test_contains_range(self):
        r_2_5_ex = IntegerRange("[2,5)")
        r_3_5_ex = IntegerRange("[3,5)")
        r_2_10_ex = IntegerRange("[2,10)")
        r_3_5_in = IntegerRange("[3,5]")
        r_7_10_ex = IntegerRange("[7,10)")
        r_3_10_ex = IntegerRange("[3,10)")

        self.assertFalse(r_2_5_ex.contains_range(r_7_10_ex))
        self.assertFalse(r_2_5_ex.contains_range(r_3_10_ex))
        self.assertFalse(r_3_5_ex.contains_range(r_2_10_ex))
        
        self.assertTrue(r_2_10_ex.contains_range(r_3_5_in))
        self.assertTrue(r_3_5_in.contains_range(r_3_5_ex))

    def test_end_points(self):
        self.assertEqual(IntegerRange("[2,6)").end_points(), {2, 5})
        self.assertEqual(IntegerRange("[2,6]").end_points(), {2, 6})
        self.assertEqual(IntegerRange("(2,6)").end_points(), {3, 5})
        self.assertEqual(IntegerRange("(2,6]").end_points(), {3, 6})

    def test_overlaps_range(self):
        r_2_5_ex = IntegerRange("[2,5)")
        r_3_5_ex = IntegerRange("[3,5)")
        r_2_10_ex = IntegerRange("[2,10)")
        r_7_10_ex = IntegerRange("[7,10)")
        r_3_10_ex = IntegerRange("[3,10)")

        self.assertFalse(r_2_5_ex.overlaps_range(r_7_10_ex))
        self.assertTrue(r_2_10_ex.overlaps_range(r_3_5_ex))
        self.assertTrue(r_3_5_ex.overlaps_range(r_3_5_ex))
        self.assertTrue(r_2_5_ex.overlaps_range(r_3_10_ex))
        self.assertTrue(r_3_5_ex.overlaps_range(r_2_10_ex))

    def test_equals(self):
        self.assertEqual(IntegerRange("[3,5)"), IntegerRange("[3,5)"))
        
        # Test de comportement avancé: [3,5) = [3,4] car ce sont les mêmes entiers {3,4}
        self.assertEqual(IntegerRange("[3,5)"), IntegerRange("[3,4]"))
        
        self.assertNotEqual(IntegerRange("[2,10)"), IntegerRange("[3,5)"))
        self.assertNotEqual(IntegerRange("[2,5)"), IntegerRange("[3,10)"))
        self.assertNotEqual(IntegerRange("[3,5)"), IntegerRange("[2,10)"))


if __name__ == '__main__':
    unittest.main()