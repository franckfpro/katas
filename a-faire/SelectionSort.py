# ==============================================================================
# KATA : Le Tri par Sélection Optimisé (Selection Sort)
# ==============================================================================
#
# CONSIGNES :
# Écrivez une fonction `selection_sort(arr)` qui prend en paramètre une liste
# d'entiers et la trie de la plus petite à la plus grande valeur.
#
# Le tri doit être effectué "en place" (il modifie directement la liste reçue).
# Pour valider facilement les tests, la fonction doit aussi retourner la liste.
#
# FONCTIONNEMENT :
# 1. Parcourez la liste pour trouver la valeur la plus basse.
# 2. Placez cette valeur la plus basse tout au début de la partie non triée.
# 3. Répétez l'opération pour le reste de la liste, autant de fois qu'il y a 
#    d'éléments à trier.
#
# CONTRAINTE D'OPTIMISATION :
# Interdiction d'utiliser les méthodes natives `pop()` et `insert()`. Elles
# provoquent des décalages d'index massifs et invisibles en mémoire. 
# Utilisez à la place une permutation directe (swap) entre le minimum trouvé
# et le premier élément de la section en cours d'analyse.
# ==============================================================================

import unittest

def selection_sort(arr: list) -> list:
    """
    Trie une liste en place à l'aide de l'algorithme du tri par sélection optimisé.
    """
    n = len(arr)
    
    # La boucle externe déplace la frontière de la sous-liste triée
    for i in range(n):
        min_index = i
        
        # La boucle interne cherche l'élément le plus petit dans le reste de la liste
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
                
        # Optimisation : Échange direct (swap) au lieu de faire un pop() + insert()
        # On échange l'élément minimal trouvé avec le premier élément non trié
        arr[i], arr[min_index] = arr[min_index], arr[i]
        
    return arr


# ==============================================================================
# SUITE DE TESTS UNITAIRES
# ==============================================================================
class TestSelectionSort(unittest.TestCase):

    def test_liste_courte(self):
        """Teste le tri d'une liste désordonnée (Premier exemple manuel)."""
        self.assertEqual(selection_sort([7, 12, 9, 11, 3]), [3, 7, 9, 11, 12])

    def test_liste_longue_avec_doublons(self):
        """Teste le tri avec la liste de l'énoncé contenant des valeurs variées."""
        mylist = [64, 34, 25, 12, 22, 11, 90, 5]
        self.assertEqual(selection_sort(mylist), [5, 11, 12, 22, 25, 34, 64, 90])

    def test_liste_deja_triee(self):
        """Vérifie que l'algorithme ne perturbe pas une liste déjà en ordre."""
        self.assertEqual(selection_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_liste_inversee(self):
        """Vérifie le tri sur une liste initialement inversée (ordre décroissant)."""
        self.assertEqual(selection_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

    def test_liste_vide_et_un_seul_element(self):
        """Cas aux limites : s'assure qu'une liste vide ou mono-élément fonctionne."""
        self.assertEqual(selection_sort([]), [])
        self.assertEqual(selection_sort([42]), [42])

    def test_valeurs_negatives(self):
        """S'assure que le tri fonctionne correctement avec des nombres négatifs."""
        self.assertEqual(selection_sort([3, -1, -5, 0, 2]), [-5, -1, 0, 2, 3])


if __name__ == '__main__':
    # Lance l'exécution des tests unitaires automatisés
    unittest.main()