import unittest

"""
KATA : ALGORITHME DE BELLMAN-FORD

À propos de ce Kata :
L'algorithme de Bellman-Ford permet de trouver les chemins les plus courts depuis 
un sommet source vers tous les autres sommets dans un graphe orienté. 

Pourquoi Bellman-Ford ?
Bien que l'algorithme de Dijkstra soit plus rapide, Bellman-Ford est indispensable 
lorsque le graphe contient des arêtes de poids négatif. Il permet également de 
détecter les "cycles négatifs" (une boucle où la somme des poids est négative, 
rendant le concept de "chemin le plus court" absurde puisqu'on pourrait y tourner 
à l'infini pour réduire le coût).

Comment ça marche (Les Règles) :
1. Initialisation : 
   - Définir la distance de la source à 0.
   - Définir la distance vers tous les autres sommets à l'infini.
   - Initialiser les prédécesseurs à None.
2. Relâchement (Relaxation) :
   - Pour chaque sommet (répéter V - 1 fois, où V est le nombre total de sommets) :
     - Parcourir toutes les arêtes du graphe.
     - Si la distance du sommet de départ + le poids de l'arête est inférieure 
       à la distance actuelle du sommet d'arrivée, mettre à jour la distance 
       et le prédécesseur.
3. Détection de cycles négatifs :
   - Parcourir une dernière fois toutes les arêtes.
   - Si une distance peut encore être réduite, cela signifie qu'il y a un cycle 
     négatif. L'algorithme doit le signaler (ex: retourner une erreur ou un flag).
"""

class Graph:
    def __init__(self, vertices):
        """
        Initialise le graphe avec une liste de sommets.
        vertices: liste des identifiants des sommets (ex: ['A', 'B', 'C', ...])
        """
        self.vertices = vertices
        self.edges = []  # Liste pour stocker les arêtes sous la forme (u, v, weight)

    def add_edge(self, u, v, weight):
        """Ajoute une arête orientée du sommet u au sommet v avec un poids."""
        self.edges.append((u, v, weight))

    def bellman_ford(self, source):
        """
        Exécute l'algorithme de Bellman-Ford depuis un sommet source.
        
        Retourne :
        - (distances, predecessors) s'il n'y a pas de cycle négatif.
        - (None, None) ou lève une exception si un cycle négatif est détecté.
        """
        # 1. Initialisation
        distances = {v: float('inf') for v in self.vertices}
        predecessors = {v: None for v in self.vertices}
        distances[source] = 0

        # 2. Relâchement (V - 1 itérations)
        for _ in range(len(self.vertices) - 1):
            for u, v, weight in self.edges:
                if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    predecessors[v] = u

        # 3. Détection de cycles négatifs
        for u, v, weight in self.edges:
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                # Un cycle négatif a été détecté
                return None, None

        return distances, predecessors

    def get_path(self, predecessors, start, end):
        """
        Reconstruit le chemin le plus court en utilisant le dictionnaire des prédécesseurs.
        """
        path = []
        current = end
        while current is not None:
            path.insert(0, current)
            if current == start:
                break
            current = predecessors[current]
        
        if not path or path[0] != start:
            return "Pas de chemin"
        return "->".join(path)


# --- TESTS UNITAIRES ---

class TestBellmanFord(unittest.TestCase):

    def setUp(self):
        # Graphe de base sans cycle négatif
        self.graph = Graph(['A', 'B', 'C', 'D', 'E'])
        self.graph.add_edge('D', 'A', 4)
        self.graph.add_edge('D', 'C', 7)
        self.graph.add_edge('D', 'E', 3)
        self.graph.add_edge('A', 'C', 4)
        self.graph.add_edge('C', 'A', -3)
        self.graph.add_edge('A', 'E', 5)
        self.graph.add_edge('E', 'C', 3)
        self.graph.add_edge('B', 'C', -4)
        self.graph.add_edge('E', 'B', 2)

    def test_shortest_paths_without_negative_cycle(self):
        distances, preds = self.graph.bellman_ford('D')
        
        # Vérification des distances minimales calculées
        self.assertIsNotNone(distances)
        self.assertEqual(distances['D'], 0)
        self.assertEqual(distances['A'], -2)
        self.assertEqual(distances['B'], 5)
        self.assertEqual(distances['C'], 1)
        self.assertEqual(distances['E'], 3)

    def test_path_reconstruction(self):
        distances, preds = self.graph.bellman_ford('D')
        
        # Le chemin le plus court de D vers A doit être D -> E -> B -> C -> A
        path_to_A = self.graph.get_path(preds, 'D', 'A')
        self.assertEqual(path_to_A, "D->E->B->C->A")

    def test_unreachable_node(self):
        # Ajouter un noeud déconnecté
        self.graph.vertices.append('Z')
        distances, preds = self.graph.bellman_ford('D')
        
        self.assertEqual(distances['Z'], float('inf'))
        self.assertEqual(self.graph.get_path(preds, 'D', 'Z'), "Pas de chemin")

    def test_negative_cycle_detection(self):
        # Création d'un graphe avec un cycle négatif explicite
        cycle_graph = Graph(['A', 'B', 'C'])
        cycle_graph.add_edge('A', 'B', 1)
        cycle_graph.add_edge('B', 'C', -1)
        cycle_graph.add_edge('C', 'A', -1) # Cycle: A -> B -> C -> A = -1
        
        distances, preds = cycle_graph.bellman_ford('A')
        
        # L'algorithme doit retourner None pour signaler le cycle négatif
        self.assertIsNone(distances)
        self.assertIsNone(preds)

if __name__ == '__main__':
    unittest.main()