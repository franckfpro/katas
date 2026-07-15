# ==============================================================================
# KATA : Le Tri à Bulles Optimisé (Bubble Sort)
# ==============================================================================
#
# CONSIGNES :
# Écrivez une fonction `bubble_sort(arr)` qui prend en paramètre une liste
# d'entiers et la trie de la plus petite à la plus grande valeur.
#
# Le tri doit être effectué "en place" (il modifie la liste d'origine). Pour
# faciliter les tests, la fonction devra également retourner la liste triée.
#
# FONCTIONNEMENT :
# 1. Parcourez la liste, une valeur à la fois.
# 2. Pour chaque élément, comparez-le avec le suivant.
# 3. Si l'élément actuel est plus grand que le suivant, permutez-les.
# 4. Répétez l'opération autant de fois qu'il y a d'éléments.
#
# OPTIMISATION REQUISE :
# Si l'algorithme parcourt la liste une fois entière sans échanger la moindre
# valeur, cela signifie que la liste est déjà triée. Interrompez alors la
# boucle principale prématurément pour économiser des ressources.
# ==============================================================================

import unittest

def bubble_sort(arr: list) -> list:
    """
    Trie une liste en place à l'aide de l'algorithme du tri à bulles optimisé.
    """
    n = len(arr)
    
    # Boucle externe pour contrôler le nombre de passages (n-1 fois au maximum)
    for i in range(n - 1):
        swapped = False
        
        # Boucle interne pour comparer les éléments adjacents.
        # À chaque passage i, le plus grand élément restant "bulle" vers sa position finale,
        # on peut donc ignorer les i derniers éléments.
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                # Permutation simultanée propre à Python (Tuple unpacking)
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                
        # Si aucun échange n'a eu lieu pendant ce tour, la liste est triée !
        if not swapped:
            break
            
    return arr


# ==============================================================================
# SUITE DE TESTS UNITAIRES
# ==============================================================================
class TestBubbleSort(unittest.TestCase):

    def test_liste_non_triee(self):
        """Teste le tri d'une liste classique désordonnée (Exemple de l'énoncé)."""
        self.assertEqual(bubble_sort([7, 12, 9, 11, 3]), [3, 7, 9, 11, 12])

    def test_liste_deja_triee(self):
        """Vérifie que l'optimisation gère correctement une liste déjà triée."""
        self.assertEqual(bubble_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_liste_inversee(self):
        """Teste le pire des cas : une liste triée dans le sens inverse."""
        self.assertEqual(bubble_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

    def test_liste_vide(self):
        """Cas aux limites : vérifie qu'une liste vide ne lève pas d'erreur."""
        self.assertEqual(bubble_sort([]), [])

    def test_un_seul_element(self):
        """Cas aux limites : vérifie qu'une liste à un élément reste inchangée."""
        self.assertEqual(bubble_sort([42]), [42])

    def test_elements_doublons(self):
        """Vérifie que l'algorithme gère correctement les valeurs identiques."""
        self.assertEqual(bubble_sort([3, 1, 3, 2, 1]), [1, 1, 2, 3, 3])


if __name__ == '__main__':
    # Exécute les tests lorsque le script est lancé directement
    unittest.main()