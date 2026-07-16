import unittest
from typing import Callable, List, Any, Optional

"""
KATA DEPTH FIRST SEARCH (Recherche en profondeur)

Description du problème :
La recherche en profondeur (DFS) n'est pas seulement une technique d'Intelligence 
Artificielle, c'est aussi la méthode standard pour parcourir des arbres 
(omniprésents en informatique).

Indices :
Pour cette forme (la plus simple) de recherche en profondeur, orientez-vous vers 
l'utilisation de la pile d'appels de fonctions (la récursivité) plutôt que vers 
une structure de données de pile manuelle. 

Essayez d'éviter d'implémenter une classe Graphe, Labyrinthe ou Problème (même 
comme une interface simulée) que votre algorithme devra parcourir. Au lieu de cela, 
posez des questions à l'environnement. Par exemple : "Quelles sont les sorties ?" 
et "Où sommes-nous ?". Cela permet des tests exploratoires plus souples et évite 
de perdre du temps à initialiser de lourdes structures de données.

Bien sûr, vous devez simuler (mocker) cette conversation dans vos tests unitaires. 
Cela démontre que les tests exploratoires peuvent être enregistrés dans des tests 
automatisés répétables.

Cas de tests suggérés :
1. Le graphe à un nœud.
2. Le graphe à deux nœuds.
3. Un labyrinthe 2x2.
4. Un arbre binaire complet à deux niveaux.
5. Un labyrinthe 3x3.
"""

def recherche_en_profondeur(
    noeud_actuel: Any, 
    cible: Any, 
    get_sorties: Callable[[Any], List[Any]], 
    chemin_parcouru: Optional[List[Any]] = None
) -> Optional[List[Any]]:
    """
    Fonction récursive effectuant une recherche en profondeur (DFS).
    
    :param noeud_actuel: La position actuelle (Où sommes-nous ?).
    :param cible: Le nœud que l'on cherche à atteindre.
    :param get_sorties: Une fonction callback qui retourne les sorties possibles 
                        pour un nœud donné (Quelles sont les sorties ?).
    :param chemin_parcouru: La liste des nœuds déjà visités pour éviter les boucles.
    :return: Une liste représentant le chemin trouvé, ou None si aucun chemin n'existe.
    """
    # Initialisation du chemin lors du premier appel
    if chemin_parcouru is None:
        chemin_parcouru = []

    # On ajoute la position actuelle au chemin
    chemin_parcouru.append(noeud_actuel)

    # Condition de sortie de succès : on a trouvé la cible
    if noeud_actuel == cible:
        return chemin_parcouru

    # On interroge l'environnement pour connaître les sorties possibles
    sorties_possibles = get_sorties(noeud_actuel)

    for sortie in sorties_possibles:
        # On ne visite pas un nœud par lequel on est déjà passé (évite les cycles)
        if sortie not in chemin_parcouru:
            # Appel récursif. On passe une copie de la liste du chemin parcouru 
            # pour que les branches de recherche n'interfèrent pas entre elles.
            resultat = recherche_en_profondeur(sortie, cible, get_sorties, list(chemin_parcouru))
            
            # Si un résultat est trouvé dans cette branche, on le remonte
            if resultat is not None:
                return resultat

    # Si aucune branche ne mène à la cible
    return None


# --- TESTS UNITAIRES ---

class TestDepthFirstSearch(unittest.TestCase):

    def generer_mock_get_sorties(self, graphe: dict) -> Callable[[Any], List[Any]]:
        """
        Fonction utilitaire pour générer notre fonction d'interrogation (le callback)
        basée sur un simple dictionnaire pour les tests.
        """
        return lambda noeud: graphe.get(noeud, [])

    def test_graphe_un_noeud(self):
        """Test avec un seul nœud qui est à la fois le départ et la cible."""
        graphe = {'A': []}
        get_sorties = self.generer_mock_get_sorties(graphe)
        
        chemin = recherche_en_profondeur('A', 'A', get_sorties)
        self.assertEqual(chemin, ['A'])

    def test_graphe_deux_noeuds(self):
        """Test simple d'un point A à un point B."""
        graphe = {
            'A': ['B'],
            'B': ['A']
        }
        get_sorties = self.generer_mock_get_sorties(graphe)
        
        chemin = recherche_en_profondeur('A', 'B', get_sorties)
        self.assertEqual(chemin, ['A', 'B'])

    def test_labyrinthe_2x2(self):
        """
        Labyrinthe 2x2 représenté par des coordonnées (x, y) :
        (0,0) -- (0,1)
          |        |
        (1,0) -- (1,1)
        """
        graphe = {
            (0, 0): [(0, 1), (1, 0)],
            (0, 1): [(0, 0), (1, 1)],
            (1, 0): [(0, 0), (1, 1)],
            (1, 1): [(0, 1), (1, 0)]
        }
        get_sorties = self.generer_mock_get_sorties(graphe)
        
        chemin = recherche_en_profondeur((0, 0), (1, 1), get_sorties)
        # La DFS va explorer la première branche trouvée. 
        # Selon l'ordre de la liste, ce sera (0,0) -> (0,1) -> (1,1)
        self.assertEqual(chemin, [(0, 0), (0, 1), (1, 1)])

    def test_arbre_binaire_complet(self):
        """
        Arbre binaire à 2 niveaux :
               A
             /   \
            B     C
           / \   / \
          D   E F   G
        """
        graphe = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['F', 'G'],
            'D': [], 'E': [], 'F': [], 'G': []
        }
        get_sorties = self.generer_mock_get_sorties(graphe)
        
        chemin = recherche_en_profondeur('A', 'F', get_sorties)
        # Pour aller à F, la DFS passera par B, réalisera que D et E mènent à des impasses,
        # remontera (backtrack) et ira dans la branche C.
        self.assertEqual(chemin, ['A', 'C', 'F'])

    def test_labyrinthe_3x3_sans_solution(self):
        """Test où la cible est inatteignable."""
        graphe = {
            1: [2, 4],
            2: [1, 3],
            3: [2],
            4: [1, 7],
            # Le noeud 5, 6, 8, 9 (cible) sont complètement isolés
            7: [4]
        }
        get_sorties = self.generer_mock_get_sorties(graphe)
        
        chemin = recherche_en_profondeur(1, 9, get_sorties)
        self.assertIsNone(chemin)

if __name__ == '__main__':
    unittest.main()