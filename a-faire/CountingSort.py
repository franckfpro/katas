import unittest

"""
KATA : TRI PAR DÉNOMBREMENT (COUNTING SORT)

Description du problème :
L'algorithme de tri par dénombrement (Counting Sort) trie un tableau en comptant 
le nombre de fois que chaque valeur apparaît. Contrairement à la plupart des 
algorithmes de tri classiques, il ne compare pas les valeurs entre elles.

Il est très rapide, mais ne fonctionne que sous certaines conditions :
1. Valeurs entières : Il se base sur le comptage d'occurrences distinctes.
2. Valeurs positives ou nulles : Les valeurs servent d'index pour le tableau 
   de comptage (un index négatif poserait problème).
3. Plage de valeurs (k) limitée : Si la valeur maximale est disproportionnée 
   par rapport au nombre d'éléments (n), le tableau de comptage prendra trop 
   de mémoire et l'algorithme deviendra inefficace.

Comment ça marche :
1. Trouvez la valeur maximale dans le tableau à trier pour définir la taille 
   du tableau de comptage.
2. Créez un tableau de comptage rempli de zéros.
3. Parcourez le tableau à trier. Pour chaque valeur `x`, incrémentez de 1 
   l'élément à l'index `x` du tableau de comptage.
4. Une fois le comptage terminé, parcourez le tableau de comptage. Pour chaque 
   index, ajoutez la valeur de l'index à votre tableau final autant de fois 
   que le compte l'indique.

Objectif du Kata :
Implémentez la fonction `tri_par_denombrement(arr)` qui prend une liste d'entiers 
positifs ou nuls et la retourne triée en utilisant la méthode décrite ci-dessus.
"""

def tri_par_denombrement(arr):
    """
    Trie une liste d'entiers positifs ou nuls en utilisant l'algorithme de 
    tri par dénombrement.
    """
    # Gérer le cas d'un tableau vide
    if not arr:
        return []
        
    # 1. Trouver la valeur maximale pour dimensionner le tableau de comptage
    valeur_max = max(arr)
    
    # 2. Créer un tableau de comptage rempli de zéros
    # La taille est valeur_max + 1 pour inclure l'index 0
    comptage = [0] * (valeur_max + 1)
    
    # 3. Compter les occurrences de chaque valeur
    for nombre in arr:
        comptage[nombre] += 1
        
    # 4. Reconstruire le tableau trié
    tableau_trie = []
    for index in range(len(comptage)):
        # Si le compte est supérieur à 0, on ajoute l'index autant de fois que nécessaire
        if comptage[index] > 0:
            tableau_trie.extend([index] * comptage[index])
            
    return tableau_trie


# --- TESTS UNITAIRES ---

class TestTriParDenombrement(unittest.TestCase):
    
    def test_exemple_manuel(self):
        """Test avec le tableau de l'exemple du cours."""
        entree = [2, 3, 0, 2, 3, 2]
        attendu = [0, 2, 2, 2, 3, 3]
        self.assertEqual(tri_par_denombrement(entree), attendu)

    def test_tableau_vide(self):
        """Un tableau vide doit retourner un tableau vide."""
        self.assertEqual(tri_par_denombrement([]), [])

    def test_un_seul_element(self):
        """Test avec un tableau ne contenant qu'un seul élément."""
        self.assertEqual(tri_par_denombrement([5]), [5])

    def test_elements_identiques(self):
        """Test avec un tableau dont tous les éléments sont identiques."""
        self.assertEqual(tri_par_denombrement([7, 7, 7, 7]), [7, 7, 7, 7])

    def test_deja_trie(self):
        """Test avec un tableau qui est déjà trié."""
        entree = [0, 1, 2, 3, 4, 5]
        self.assertEqual(tri_par_denombrement(entree), entree)

if __name__ == '__main__':
    unittest.main()
