import unittest

"""
KATA : TRI FUSION (MERGE SORT)

Description du problème :
L'algorithme de Tri Fusion (Merge Sort) est un algorithme de type "Diviser pour Régner" 
(Divide and Conquer). Il trie un tableau en le décomposant d'abord en sous-tableaux 
plus petits, puis en les reconstruisant dans le bon ordre pour obtenir un tableau trié.

Comment ça marche (Approche Récursive) :
1. Diviser (Divide) : Séparez le tableau non trié en deux sous-tableaux de taille 
   environ égale.
2. Continuez à diviser récursivement les sous-tableaux jusqu'à ce que chaque 
   sous-tableau ne contienne plus qu'un seul élément (un tableau d'un élément est 
   considéré comme trié).
3. Régner (Conquer / Merge) : Fusionnez les sous-tableaux deux par deux en comparant 
   leurs éléments pour toujours placer la valeur la plus basse en premier.
4. Continuez la fusion jusqu'à ce qu'il ne reste qu'un seul tableau trié complet.

Objectif du Kata :
Implémentez la fonction `tri_fusion(arr)` qui trie une liste d'éléments (entiers 
ou flottants) en utilisant l'algorithme récursif détaillé ci-dessus. Vous aurez 
probablement besoin d'une fonction d'aide pour fusionner deux listes triées.
"""

def fusionner(gauche: list, droite: list) -> list:
    """
    Fonction d'aide pour fusionner deux sous-tableaux déjà triés.
    """
    resultat = []
    i = 0 # Index pour le tableau de gauche
    j = 0 # Index pour le tableau de droite

    # On compare les éléments des deux tableaux et on insère le plus petit
    while i < len(gauche) and j < len(droite):
        if gauche[i] < droite[j]:
            resultat.append(gauche[i])
            i += 1
        else:
            resultat.append(droite[j])
            j += 1

    # S'il reste des éléments dans l'un des tableaux, on les ajoute à la fin.
    # (Puisque les sous-tableaux sont déjà triés, on peut juste les ajouter).
    resultat.extend(gauche[i:])
    resultat.extend(droite[j:])

    return resultat

def tri_fusion(arr: list) -> list:
    """
    Fonction principale récursive implémentant le Tri Fusion.
    """
    # Cas de base : un tableau de 1 élément ou vide est déjà trié
    if len(arr) <= 1:
        return arr

    # Diviser : Trouver le milieu
    milieu = len(arr) // 2
    
    # Créer les deux moitiés
    moitie_gauche = arr[:milieu]
    moitie_droite = arr[milieu:]

    # Appel récursif pour trier les deux moitiés
    gauche_triee = tri_fusion(moitie_gauche)
    droite_triee = tri_fusion(moitie_droite)

    # Régner : Fusionner les deux moitiés triées
    return fusionner(gauche_triee, droite_triee)


# --- TESTS UNITAIRES ---

class TestTriFusion(unittest.TestCase):
    
    def test_exemple_cours(self):
        """Test basé sur l'exemple final du cours."""
        entree = [3, 7, 6, -10, 15, 23.5, 55, -13]
        attendu = [-13, -10, 3, 6, 7, 15, 23.5, 55]
        self.assertEqual(tri_fusion(entree), attendu)

    def test_tableau_vide(self):
        """Un tableau vide doit retourner un tableau vide."""
        self.assertEqual(tri_fusion([]), [])

    def test_un_seul_element(self):
        """Un tableau avec un seul élément est déjà trié."""
        self.assertEqual(tri_fusion([42]), [42])

    def test_deja_trie(self):
        """Test avec un tableau qui est déjà dans le bon ordre."""
        entree = [1, 2, 3, 4, 5]
        self.assertEqual(tri_fusion(entree), [1, 2, 3, 4, 5])

    def test_ordre_inverse(self):
        """Test avec un tableau trié dans l'ordre inverse."""
        entree = [5, 4, 3, 2, 1]
        self.assertEqual(tri_fusion(entree), [1, 2, 3, 4, 5])

    def test_elements_en_double(self):
        """Test avec des éléments apparaissant plusieurs fois."""
        entree = [4, 2, 2, 8, 3, 3, 1]
        attendu = [1, 2, 2, 3, 3, 4, 8]
        self.assertEqual(tri_fusion(entree), attendu)

    def test_taille_impaire(self):
        """Test avec un tableau dont la taille ne se divise pas parfaitement en deux."""
        entree = [12, 8, 9, 3, 11, 5, 4]
        attendu = [3, 4, 5, 8, 9, 11, 12]
        self.assertEqual(tri_fusion(entree), attendu)


if __name__ == '__main__':
    unittest.main()