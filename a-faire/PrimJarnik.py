import sys
import unittest

# =============================================================================
# KATA : ALGORITHME DE PRIM-JARNÍK
# =============================================================================
#
# CONSIGNES :
# L'algorithme de Prim trouve l'Arbre Couvrant de Poids Minimum (MST) dans
# un graphe non orienté et connexe. Le MST est l'ensemble des arêtes qui
# connectent tous les sommets avec la somme des poids la plus faible possible.
#
# Comment ça marche :
# 1. Choisissez un sommet de départ au hasard et incluez-le comme premier
#    sommet du MST.
# 2. Comparez les arêtes sortant des sommets actuellement dans le MST.
# 3. Choisissez l'arête avec le poids le plus faible qui connecte un sommet
#    du MST à un sommet en dehors du MST.
# 4. Ajoutez cette arête et ce sommet au MST.
# 5. Répétez les étapes 2 et 3 jusqu'à ce que tous les sommets fassent partie
#    du MST.
#
# Note : Étant donné que le sommet de départ peut être choisi au hasard ou 
# fixé (ici l'index 0), l'ordre d'ajout des arêtes peut varier, mais le poids
# total minimum du MST restera toujours le même.
# =============================================================================

class Graph:
    def __init__(self, size):
        """Initialise le graphe avec une taille donnée via une matrice d'adjacence."""
        self.size = size
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.vertex_data = [''] * size

    def add_vertex_data(self, vertex, data):
        """Assigne un nom (data) à un sommet donné par son index."""
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def add_edge(self, u, v, weight):
        """Ajoute une arête non orientée avec un poids entre les sommets u et v."""
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = weight
            self.adj_matrix[v][u] = weight  # Le graphe est non orienté

    def prims_algorithm(self, start_vertex=0):
        """
        Exécute l'algorithme de Prim à partir d'un sommet de départ 
        et retourne la liste des arêtes formant le MST.
        """
        # in_mst garde la trace des sommets déjà inclus dans l'arbre
        in_mst = [False] * self.size
        
        # key_values stocke la distance minimale connue pour atteindre chaque sommet
        key_values = [sys.maxsize] * self.size
        
        # parents stocke l'arbre couvrant résultant (qui est le parent de qui)
        parents = [-1] * self.size

        # Initialisation du sommet de départ
        key_values[start_vertex] = 0

        # On boucle pour ajouter (V - 1) arêtes au MST
        for _ in range(self.size - 1):
            
            # Étape 1 : Trouver le sommet avec la plus petite valeur de clé 
            # parmi ceux qui ne sont pas encore dans le MST
            min_key = sys.maxsize
            u = -1
            for i in range(self.size):
                if not in_mst[i] and key_values[i] < min_key:
                    min_key = key_values[i]
                    u = i

            # Si on ne trouve pas de sommet connectable, le graphe est déconnecté
            if u == -1:
                break

            # Ajouter le sommet sélectionné au MST
            in_mst[u] = True

            # Étape 2 & 3 : Mettre à jour les valeurs de clé et les parents
            # des sommets adjacents au sommet fraîchement ajouté
            for v in range(self.size):
                weight = self.adj_matrix[u][v]
                # S'il y a une arête (weight > 0), que le sommet n'est pas dans le MST
                # et que ce poids est inférieur à la meilleure distance connue pour v
                if weight > 0 and not in_mst[v] and weight < key_values[v]:
                    key_values[v] = weight
                    parents[v] = u

        # Construction du résultat final sous forme de liste de tuples (parent, sommet, poids)
        mst_edges = []
        for i in range(self.size):
            if parents[i] != -1:
                mst_edges.append((parents[i], i, self.adj_matrix[parents[i]][i]))
                
        return mst_edges


# =============================================================================
# TESTS UNITAIRES
# =============================================================================

class TestPrimAlgorithm(unittest.TestCase):

    def setUp(self):
        """Initialise le graphe décrit dans l'exemple manuel du Kata."""
        self.g = Graph(8)
        self.g.add_vertex_data(0, 'A')
        self.g.add_vertex_data(1, 'B')
        self.g.add_vertex_data(2, 'C')
        self.g.add_vertex_data(3, 'D')
        self.g.add_vertex_data(4, 'E')
        self.g.add_vertex_data(5, 'F')
        self.g.add_vertex_data(6, 'G')
        self.g.add_vertex_data(7, 'H')

        self.g.add_edge(0, 1, 4)  # A - B
        self.g.add_edge(0, 3, 3)  # A - D
        self.g.add_edge(1, 2, 3)  # B - C
        self.g.add_edge(1, 3, 5)  # B - D
        self.g.add_edge(1, 4, 6)  # B - E
        self.g.add_edge(2, 4, 4)  # C - E
        self.g.add_edge(2, 7, 2)  # C - H
        self.g.add_edge(3, 4, 7)  # D - E
        self.g.add_edge(3, 5, 4)  # D - F
        self.g.add_edge(4, 5, 5)  # E - F
        self.g.add_edge(4, 6, 3)  # E - G
        self.g.add_edge(5, 6, 7)  # F - G
        self.g.add_edge(6, 7, 5)  # G - H

    def test_prim_total_weight(self):
        """Valide que le poids total du MST est correct."""
        mst = self.g.prims_algorithm(start_vertex=0)
        
        # Le poids total attendu pour ce graphe est 23
        total_weight = sum([weight for u, v, weight in mst])
        self.assertEqual(total_weight, 23)

    def test_prim_edge_count(self):
        """Valide que le nombre d'arêtes sélectionnées est bien (V - 1)."""
        mst = self.g.prims_algorithm(start_vertex=0)
        self.assertEqual(len(mst), 7)

    def test_prim_starts_from_different_node(self):
        """Valide que démarrer d'un sommet différent donne le même poids total."""
        mst = self.g.prims_algorithm(start_vertex=4) # Démarrer par 'E' (index 4)
        total_weight = sum([weight for u, v, weight in mst])
        self.assertEqual(total_weight, 23)

if __name__ == '__main__':
    unittest.main()