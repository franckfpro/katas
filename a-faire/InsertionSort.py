# ==============================================================================
# KATA : Le Tri par Insertion Optimisé (Insertion Sort)
# ==============================================================================
#
# CONSIGNES :
# Écrivez une fonction `insertion_sort(arr)` qui prend en paramètre une liste
# d'entiers et la trie de la plus petite à la plus grande valeur.
#
# Le tri doit être effectué "en place" (il modifie la liste d'origine). Pour
# faciliter la validation, la fonction devra également retourner la liste triée.
#
# FONCTIONNEMENT :
# 1. Considérez le premier élément comme faisant déjà partie d'une liste triée.
# 2. Prenez l'élément suivant (issu de la partie non triée).
# 3. Comparez-le aux éléments de la partie triée en remontant de droite à gauche.
# 4. Insérez-le à sa position correcte.
# 5. Répétez l'opération pour tous les éléments de la liste.
#
# CONTRAINTE DE PERFORMANCE (L'optimisation) :
# N'utilisez pas les méthodes natives `pop()` et `insert()` de Python. 
# Ces méthodes effectuent des décalages de mémoire superflus en arrière-plan. 
# À la place, mémorisez la valeur actuelle, décalez les éléments plus grands 
# d'une case vers la droite, et déposez votre valeur à l'emplacement libéré.
# ==============================================================================

import unittest

def insertion_sort(arr: list) -> list:
    """
    Trie une liste en place à l'aide de l'algorithme du tri par insertion optimisé.
    """
    n = len(arr)
    
    # La boucle externe commence à 1 car un seul élément (à l'index 0) est déjà trié.
    for i in range(1, n):
        insert_index = i
        current_value = arr[i]
        
        # La boucle interne remonte la partie triée (de i-1 jusqu'à 0)
        for j in range(i - 1, -1, -1):
            if arr[j] > current_value:
                # Décale l'élément vers la droite pour faire de la place
                arr[j + 1] = arr[j]
                insert_index = j
            else:
                # Si l'élément est plus petit ou égal, on a trouvé le point d'insertion
                break
                
        # Place la valeur mémorisée à son index définitif pour ce tour
        arr[insert_index] = current_value
        
    return arr


# ==============================================================================
# SUITE DE TESTS UNITAIRES
# ==============================================================================
class TestInsertionSort(unittest.TestCase):

    def test_liste_desordonnee(self):
        """Teste le tri d'une liste désordonnée standard (Exemple de l'énoncé)."""
        self.assertEqual(insertion_sort([7, 12, 9, 11, 3]), [3, 7, 9, 11, 12])

    def test_liste_w3schools_exemple(self):
        """Teste l'algorithme avec une liste plus longue comportant des doublons."""
        mylist = [64, 34, 25, 12, 22, 11, 90, 5]
        self.assertEqual(insertion_sort(mylist), [5, 11, 12, 22, 25, 34, 64, 90])

    def test_liste_deja_triee(self):
        """Vérifie le comportement et la rapidité sur une liste déjà triée (meilleur des cas)."""
        self.assertEqual(insertion_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_liste_inversee(self):
        """Teste le pire des cas : une liste triée dans l'ordre décroissant."""
        self.assertEqual(insertion_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

    def test_liste_vide_et_monoelement(self):
        """Cas aux limites : listes vides ou contenant un seul élément."""
        self.assertEqual(insertion_sort([]), [])
        self.assertEqual(insertion_sort([42]), [42])

    def test_valeurs_negatives(self):
        """S'assure que l'algorithme prend correctement en compte les nombres négatifs."""
        self.assertEqual(insertion_sort([3, -1, 0, -5, 2]), [-5, -1, 0, 2, 3])


if __name__ == '__main__':
    # Lance la suite de tests à l'exécution du script
    unittest.main()