import unittest

# =====================================================================
# KATA : MANHATTAN DISTANCE
# =====================================================================
#
# CONSIGNES :
# La distance de Manhattan est la distance entre deux points dans une
# grille (comme la géographie des rues en forme de grille de 
# l'arrondissement de Manhattan à New York) calculée en n'empruntant
# qu'un chemin vertical et/ou horizontal.
# Formule mathématique : $d = |x_1 - x_2| + |y_1 - y_2|$
#
# Écrire une fonction `manhattan_distance(p1, p2)` qui renvoie la 
# distance de Manhattan entre les deux points.
#
# Contraintes de conception :
# - La classe Point est immuable.
# - La classe Point n'a pas de Getters, ni de Setters.
# - La classe Point n'a pas de propriétés publiques (c'est-à-dire que
#   l'état interne ne peut pas être lu de l'extérieur de la classe).
# =====================================================================

class Point:
    """
    Représente un point sur une grille. 
    Les coordonnées sont strictement privées pour respecter les contraintes.
    """
    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y

    # L'astuce pour respecter la règle "Pas de propriétés publiques" 
    # et "Pas de Getters" consiste à utiliser le Double Dispatch. 
    # On demande à un point de calculer la distance avec un autre point 
    # en lui transmettant ses propres coordonnées internes privées.
    def calculate_distance_with(self, other_point: 'Point') -> int:
        return other_point._distance_from_coordinates(self.__x, self.__y)

    # Méthode "protégée" (convention) qui effectue le calcul réel.
    def _distance_from_coordinates(self, x: int, y: int) -> int:
        return abs(self.__x - x) + abs(self.__y - y)


def manhattan_distance(p1: Point, p2: Point) -> int:
    """
    Calcule la distance de Manhattan entre deux points.
    Délègue l'opération aux objets pour préserver leur encapsulation.
    """
    return p1.calculate_distance_with(p2)


# =====================================================================
# TESTS UNITAIRES
# =====================================================================

class TestManhattanDistance(unittest.TestCase):

    def test_distance_meme_point(self):
        """manhattanDistance( Point(1, 1), Point(1, 1) ) doit retourner 0."""
        p1 = Point(1, 1)
        p2 = Point(1, 1)
        self.assertEqual(manhattan_distance(p1, p2), 0)

    def test_distance_points_eloignes_positifs(self):
        """manhattanDistance( Point(5, 4), Point(3, 2) ) doit retourner 4."""
        p1 = Point(5, 4)
        p2 = Point(3, 2)
        self.assertEqual(manhattan_distance(p1, p2), 4)

    def test_distance_avec_zero(self):
        """manhattanDistance( Point(1, 1), Point(0, 3) ) doit retourner 3."""
        p1 = Point(1, 1)
        p2 = Point(0, 3)
        self.assertEqual(manhattan_distance(p1, p2), 3)

    def test_distance_bidirectionnelle(self):
        """La distance doit être identique peu importe l'ordre des arguments."""
        p1 = Point(5, 4)
        p2 = Point(3, 2)
        self.assertEqual(manhattan_distance(p1, p2), manhattan_distance(p2, p1))
        
    def test_distance_coordonnees_negatives(self):
        """Doit fonctionner correctement même avec des coordonnées négatives sur la grille."""
        p1 = Point(-2, -1)
        p2 = Point(2, 2)
        # |-2 - 2| + |-1 - 2| = |-4| + |-3| = 4 + 3 = 7
        self.assertEqual(manhattan_distance(p1, p2), 7)


if __name__ == '__main__':
    unittest.main()