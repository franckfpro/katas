import unittest

# ==========================================
# CONSIGNES DU KATA : RECHERCHE DICHOTOMIQUE
# ==========================================
# Objectif : Implémenter l'algorithme de recherche dichotomique (Binary Search).
# 
# Pour implémenter cet algorithme, voici ce dont vous avez besoin :
# - Un tableau (liste) contenant des valeurs triées dans lequel chercher.
# - Une valeur cible (target_val) à rechercher.
# - Une boucle qui s'exécute tant que l'index "gauche" (left) est inférieur 
#   ou égal à l'index "droit" (right).
# - Une condition (if) qui compare la valeur du milieu avec la valeur cible, 
#   et retourne l'index si la valeur cible est trouvée.
# - Une condition (if) qui vérifie si la valeur cible est inférieure ou supérieure 
#   à la valeur du milieu, et met à jour les variables "gauche" ou "droite" 
#   pour réduire la zone de recherche de moitié.
# - Après la boucle, retourner -1, car à ce stade, nous savons que la valeur 
#   cible n'a pas été trouvée dans le tableau.
# ==========================================

def binary_search(arr, target_val):
    """
    Effectue une recherche dichotomique pour trouver target_val dans arr.
    Retourne l'index de la valeur si elle est trouvée, sinon retourne -1.
    """
    left = 0
    right = len(arr) - 1

    while left <= right:
        # On calcule l'index du milieu (division entière)
        mid = (left + right) // 2

        # Si la cible est au milieu, on a trouvé !
        if arr[mid] == target_val:
            return mid

        # Si la valeur du milieu est plus petite que la cible,
        # on ignore la moitié gauche.
        if arr[mid] < target_val:
            left = mid + 1
        # Sinon, la valeur du milieu est plus grande que la cible,
        # on ignore la moitié droite.
        else:
            right = mid - 1

    # La boucle s'est terminée sans trouver la valeur
    return -1


# ==========================================
# TESTS UNITAIRES
# ==========================================
class TestBinarySearch(unittest.TestCase):
    def setUp(self):
        # Liste de test triée obligatoire pour la recherche dichotomique
        self.mylist = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

    def test_value_found_in_middle(self):
        self.assertEqual(binary_search(self.mylist, 11), 5)

    def test_value_found_at_start(self):
        self.assertEqual(binary_search(self.mylist, 1), 0)

    def test_value_found_at_end(self):
        self.assertEqual(binary_search(self.mylist, 19), 9)

    def test_value_not_found_less_than_min(self):
        self.assertEqual(binary_search(self.mylist, 0), -1)

    def test_value_not_found_greater_than_max(self):
        self.assertEqual(binary_search(self.mylist, 25), -1)

    def test_value_not_found_in_between(self):
        self.assertEqual(binary_search(self.mylist, 8), -1)

    def test_empty_list(self):
        self.assertEqual(binary_search([], 5), -1)

if __name__ == '__main__':
    # Lance les tests si le script est exécuté directement
    unittest.main()