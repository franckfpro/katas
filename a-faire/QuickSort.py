# ==============================================================================
# KATA : Le Tri Rapide (Quicksort)
# ==============================================================================
#
# CONSIGNES :
# Écrivez une fonction récursive `quicksort(array)` qui trie une liste d'entiers
# du plus petit au plus grand.
#
# L'algorithme doit utiliser le principe du "Tri Rapide" en choisissant le
# DERNIER élément de la liste (ou sous-liste) comme élément "pivot".
#
# FONCTIONNEMENT :
# 1. Partitionnement : Organisez la liste de manière à ce que toutes les valeurs
#    inférieures ou égales au pivot soient à sa gauche, et toutes les valeurs
#    supérieures soient à sa droite.
# 2. Placement du pivot : Insérez le pivot à sa place définitive, entre les 
#    valeurs inférieures et supérieures.
# 3. Récursion : Appliquez de manière récursive la même opération sur la 
#    sous-liste de gauche et sur la sous-liste de droite.
# 4. Condition d'arrêt : La récursion s'arrête lorsque les sous-listes ont une
#    taille inférieure ou égale à 1 (elles sont alors déjà triées).
#
# Le tri doit être effectué "en place" (modification directe de la liste reçue).
# ==============================================================================

import unittest

def partition(array: list, low: int, high: int) -> int:
    """
    Positionne le pivot (dernier élément) à sa place définitive.
    Place les éléments plus petits à gauche et les plus grands à droite.
    Retourne l'index final du pivot.
    """
    pivot = array[high]
    i = low - 1  # Index du plus grand élément parmi les plus petits que le pivot

    for j in range(low, high):
        # Si l'élément actuel est inférieur ou égal au pivot
        if array[j] <= pivot:
            i += 1
            # Échange des éléments pour amener le plus petit à gauche
            array[i], array[j] = array[j], array[i]

    # Place le pivot juste après le bloc des éléments plus petits
    array[i + 1], array[high] = array[high], array[i + 1]
    return i + 1


def quicksort(array: list, low: int = 0, high: int = None) -> list:
    """
    Trie une liste en place à l'aide de l'algorithme Quicksort.
    Les arguments 'low' et 'high' permettent de cibler les sous-listes lors des appels récursifs.
    """
    # Initialisation des index lors du premier appel
    if high is None:
        high = len(array) - 1

    # Condition de base : la sous-liste doit contenir au moins 2 éléments pour être triée
    if low < high:
        # Recherche de l'index de partition (le pivot est désormais à sa place)
        pivot_index = partition(array, low, high)

        # Appels récursifs pour la partie gauche et la partie droite du pivot
        quicksort(array, low, pivot_index - 1)
        quicksort(array, pivot_index + 1, high)

    return array


# ==============================================================================
# SUITE DE TESTS UNITAIRES
# ==============================================================================
class TestQuicksort(unittest.TestCase):

    def test_liste_desordonnee_courte(self):
        """Teste le tri avec l'exemple de l'énoncé manuel."""
        self.assertEqual(quicksort([11, 9, 12, 7, 3]), [3, 7, 9, 11, 12])

    def test_liste_desordonnee_longue(self):
        """Teste le tri avec l'exemple de code fourni (mylist)."""
        mylist = [64, 34, 25, 5, 22, 11, 90, 12]
        self.assertEqual(quicksort(mylist), [5, 11, 12, 22, 25, 34, 64, 90])

    def test_liste_deja_triee(self):
        """Vérifie qu'une liste déjà triée reste intacte."""
        self.assertEqual(quicksort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_liste_inversee(self):
        """Vérifie le tri d'une liste triée dans l'ordre décroissant."""
        self.assertEqual(quicksort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

    def test_liste_vide_et_monoelement(self):
        """Cas aux limites : s'assure qu'une liste vide ou à un seul élément ne plante pas."""
        self.assertEqual(quicksort([]), [])
        self.assertEqual(quicksort([42]), [42])

    def test_valeurs_doublons(self):
        """Vérifie la stabilité de la comparaison face à des valeurs identiques."""
        self.assertEqual(quicksort([12, 5, 12, 7, 5]), [5, 5, 7, 12, 12])


if __name__ == '__main__':
    # Déclenche l'exécution des tests unitaires
    unittest.main()