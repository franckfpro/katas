import unittest

# =============================================================================
# KATA : ALGORITHME DE KRUSKAL
# =============================================================================
#
# CONSIGNES :
# L'algorithme de Kruskal trouve l'Arbre Couvrant de Poids Minimum (MST) ou 
# une Forêt Couvrante dans un graphe non orienté. Le MST est l'ensemble 
# des arêtes qui connectent tous les sommets avec le poids total minimum.
#
# Comment ça marche :
# 1. Triez les arêtes du graphe du poids le plus faible au plus élevé.
# 2. Pour chaque arête (en commençant par la plus petite) :
#    - Cette arête créera-t-elle un cycle dans le MST actuel ?
#    - Si non : Ajoutez l'arête au MST.
# 3. Répétez jusqu'à ce que tous les sommets soient couverts.
#
# Pour détecter les cycles efficacement, nous utilisons la méthode "Union-Find" 
# (Recherche et Union) avec un tableau de parents (parent array) et 
# d'optimisation de rang (rank array).
# =============================================================================

class Graph:
    def __init__(self, size):
        """Initialise le graphe avec une taille donnée."""
        self.size = size
        self.edges = [] 
        self.vertex_data = [''] * size

    def add_vertex_data(self, vertex, data):
        """Ajoute un nom ou une donnée à un sommet."""
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def add_edge(self, u, v, weight):
        """Ajoute une arête non orientée au graphe."""
        self.edges.append((weight, u, v))

    def find(self, parent, i):
        """
        Trouve la racine du sommet i (avec compression de chemin).
        Utilisé pour vérifier à quel sous-ensemble appartient un sommet.
        """
        if parent[i] == i:
            return i
        parent[i] = self.find(parent, parent[i])
        return parent[i]

    def union(self, parent, rank, x, y):
        """
        Unit les deux sous-ensembles x et y en utilisant le rang 
        pour garder un arbre plat.
        """
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)

        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def kruskals_algorithm(self):
        """
        Exécute l'algorithme de Kruskal et retourne la liste des arêtes 
        formant le MST (ou la forêt couvrante).
        """
        result = []  # Stocke le MST final
        
        # Étape 1 : Trier les arêtes par poids croissant
        self.edges = sorted(self.edges, key=lambda item: item[0])
        
        parent = []
        rank = []
        
        # Initialisation de Union-Find : chaque sommet est son propre parent
        for node in range(self.size):
            parent.append(node)
            rank.append(0)
            
        i = 0  # Index pour parcourir les arêtes triées
        
        # Étape 2 & 3 : Parcourir les arêtes et construire le MST
        # On continue jusqu'à ce qu'on ait évalué toutes les arêtes.
        # Note : Pour un graphe connexe pur, on pourrait s'arrêter quand len(result) == self.size - 1.
        while i < len(self.edges):
            weight, u, v = self.edges[i]
            i += 1
            
            x = self.find(parent, u)
            y = self.find(parent, v)
            
            # S'il n'y a pas de cycle (les racines sont différentes), on ajoute au résultat
            if x != y:
                result.append((weight, u, v))
                self.union(parent, rank, x, y)
                
        return result


# =============================================================================
# TESTS UNITAIRES
# =============================================================================

class TestKruskalAlgorithm(unittest.TestCase):

    def test_kruskal_standard_graph(self):
        """Test basé sur le cas d'usage classique de l'énoncé."""
        g = Graph(7)
        g.add_vertex_data(0, 'A')
        g.add_vertex_data(1, 'B')
        g.add_vertex_data(2, 'C')
        g.add_vertex_data(3, 'D')
        g.add_vertex_data(4, 'E')
        g.add_vertex_data(5, 'F')
        g.add_vertex_data(6, 'G')

        g.add_edge(0, 1, 4)   # A-B, 4
        g.add_edge(0, 6, 10)  # A-G, 10
        g.add_edge(0, 2, 9)   # A-C, 9
        g.add_edge(1, 2, 8)   # B-C, 8
        g.add_edge(2, 3, 5)   # C-D, 5
        g.add_edge(2, 4, 2)   # C-E, 2
        g.add_edge(2, 6, 7)   # C-G, 7
        g.add_edge(3, 4, 3)   # D-E, 3
        g.add_edge(3, 5, 7)   # D-F, 7
        g.add_edge(4, 6, 6)   # E-G, 6
        g.add_edge(5, 6, 11)  # F-G, 11

        mst = g.kruskals_algorithm()
        
        # Le poids total attendu pour ce MST spécifique est 27
        # Arêtes attendues (poids, u, v) : (2, C, E), (3, D, E), (4, A, B), (6, E, G), (7, D, F), (5, C, D)... 
        # (L'ordre de sélection exact gère les égalités et ne retient pas les cycles)
        total_weight = sum([weight for weight, u, v in mst])
        self.assertEqual(total_weight, 27)
        
        # Il doit y avoir exactement (V - 1) arêtes pour un graphe connexe
        self.assertEqual(len(mst), 6)

    def test_kruskal_disconnected_graph(self):
        """Test avec un graphe non connexe (Minimum Spanning Forest)."""
        g = Graph(4)
        # Graphe divisé en 2 sous-graphes : {0, 1} et {2, 3}
        g.add_edge(0, 1, 10)
        g.add_edge(2, 3, 5)
        
        mst = g.kruskals_algorithm()
        
        # Le poids total attendu est 15
        total_weight = sum([weight for weight, u, v in mst])
        self.assertEqual(total_weight, 15)
        
        # Il doit y avoir exactement 2 arêtes sélectionnées (V - 2 ici car 2 composantes)
        self.assertEqual(len(mst), 2)

if __name__ == '__main__':
    unittest.main()