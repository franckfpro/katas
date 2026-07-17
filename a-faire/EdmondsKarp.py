import unittest
from collections import deque

# =====================================================================
# CONSIGNES DU KATA : ALGORITHME D'EDMONDS-KARP
# =====================================================================
# L'algorithme d'Edmonds-Karp résout le problème du flot maximum dans 
# un graphe orienté.
# 
# Le flot part d'un sommet source (s) et se termine dans un sommet 
# puits (t). Chaque arête du graphe permet un certain flot, limité 
# par une capacité.
#
# L'objectif de ce Kata est d'implémenter cet algorithme en utilisant 
# un parcours en largeur (BFS - Breadth-First Search) pour trouver 
# des chemins augmentants.
#
# Règles de l'algorithme :
# 1. Commencer avec un flot de zéro sur toutes les arêtes.
# 2. Utiliser BFS pour trouver un chemin augmentant (une capacité 
#    disponible) de la source au puits.
# 3. Faire un calcul de "goulot d'étranglement" pour savoir quel flot 
#    maximum peut être envoyé sur ce chemin.
# 4. Augmenter le flot le long du chemin (et réduire la capacité 
#    résiduelle).
# 5. Ajouter cette même valeur à la capacité des arêtes inverses pour 
#    permettre "d'annuler" un flot si nécessaire.
# 6. Répéter les étapes 2 à 4 jusqu'à ce qu'il n'y ait plus de chemin 
#    augmentant possible.
# =====================================================================

class Graph:
    def __init__(self, size: int):
        """Initialise un graphe avec un nombre donné de sommets."""
        self.size = size
        # La matrice d'adjacence stocke les capacités résiduelles
        self.adj_matrix = [[0] * size for _ in range(size)]
        
    def add_edge(self, u: int, v: int, capacity: int):
        """Ajoute une arête dirigée de u vers v avec une capacité donnée."""
        self.adj_matrix[u][v] = capacity

    def bfs(self, source: int, sink: int, parent: list[int]) -> bool:
        """
        Trouve un chemin augmentant de la source au puits en utilisant BFS.
        Met à jour le tableau 'parent' pour reconstruire le chemin.
        Retourne True si un chemin est trouvé, False sinon.
        """
        visited = [False] * self.size
        queue = deque([source])
        visited[source] = True
        
        while queue:
            u = queue.popleft()
            
            for v, capacity in enumerate(self.adj_matrix[u]):
                # Si le sommet n'est pas visité et qu'il y a une capacité résiduelle
                if not visited[v] and capacity > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    
                    # Si on atteint le puits, on peut arrêter la recherche
                    if v == sink:
                        return True
        return False

    def edmonds_karp(self, source: int, sink: int) -> int:
        """
        Calcule et retourne le flot maximum de la source au puits.
        """
        parent = [-1] * self.size
        max_flow = 0
        
        # Tant qu'il existe un chemin augmentant
        while self.bfs(source, sink, parent):
            path_flow = float('Inf')
            s = sink
            
            # 1. Trouver la capacité résiduelle minimale (le goulot d'étranglement)
            while s != source:
                p = parent[s]
                path_flow = min(path_flow, self.adj_matrix[p][s])
                s = p
                
            max_flow += path_flow
            
            # 2. Mettre à jour les capacités résiduelles des arêtes normales et inverses
            v = sink
            while v != source:
                u = parent[v]
                self.adj_matrix[u][v] -= path_flow
                self.adj_matrix[v][u] += path_flow  # Ajout de la capacité à l'arête inverse
                v = u
                
        return max_flow


# =====================================================================
# TESTS UNITAIRES
# =====================================================================
class TestEdmondsKarp(unittest.TestCase):

    def test_example_from_kata(self):
        # Le graphe d'exemple de l'énoncé avec 6 sommets (s, v1, v2, v3, v4, t)
        g = Graph(6)
        
        # Index : 0=s, 1=v1, 2=v2, 3=v3, 4=v4, 5=t
        g.add_edge(0, 1, 3)
        g.add_edge(0, 2, 7)
        g.add_edge(1, 3, 3)
        g.add_edge(1, 4, 4)
        g.add_edge(2, 1, 5)
        g.add_edge(2, 4, 3)
        g.add_edge(3, 4, 3)
        g.add_edge(3, 5, 2)
        g.add_edge(4, 5, 6)
        
        # Le flot maximum attendu est 8
        self.assertEqual(g.edmonds_karp(0, 5), 8)

    def test_simple_linear_graph(self):
        # Un graphe linéaire simple : 0 -> 1 -> 2
        g = Graph(3)
        g.add_edge(0, 1, 10)
        g.add_edge(1, 2, 10)
        
        self.assertEqual(g.edmonds_karp(0, 2), 10)

    def test_graph_with_bottleneck(self):
        # Graphe avec un goulot d'étranglement évident
        g = Graph(4)
        g.add_edge(0, 1, 100)
        g.add_edge(1, 2, 1)    # Goulot d'étranglement
        g.add_edge(2, 3, 100)
        
        self.assertEqual(g.edmonds_karp(0, 3), 1)

    def test_disconnected_graph(self):
        # Graphe où la source et le puits ne sont pas connectés
        g = Graph(4)
        g.add_edge(0, 1, 10)
        g.add_edge(2, 3, 10)
        
        self.assertEqual(g.edmonds_karp(0, 3), 0)


if __name__ == '__main__':
    unittest.main()