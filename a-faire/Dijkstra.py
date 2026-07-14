import unittest

"""
KATA : ALGORITHME DE DIJKSTRA

À propos de ce Kata :
L'algorithme de Dijkstra permet de trouver le chemin le plus court depuis un sommet 
source (départ) vers tous les autres sommets d'un graphe orienté ou non orienté.
Attention : cet algorithme ne fonctionne pas si le graphe contient des arêtes avec 
des poids négatifs (pour cela, il faudrait utiliser Bellman-Ford).

Complexité :
Dans son implémentation basique (sans file de priorité), sa complexité en temps 
est de $O(V^2)$, où $V$ est le nombre de sommets.

Les Règles du Kata (Comment ça marche) :
1. Initialisation : 
   - Assigner à chaque sommet une distance initiale : 0 pour le sommet de départ, 
     et l'infini (float('inf')) pour tous les autres.
   - Créer un dictionnaire pour garder la trace du sommet "prédécesseur" (pour 
     reconstruire le chemin final).
   - Garder une trace des sommets visités (ex: un Set).
2. Traitement :
   - Tant qu'il reste des sommets non visités :
     a. Choisir le sommet non visité ayant la plus petite distance calculée.
     b. Pour chaque voisin de ce sommet : calculer la distance totale depuis le départ 
        (distance du sommet actuel + poids de l'arête vers le voisin).
     c. Si cette distance calculée est strictement inférieure à la distance 
        actuellement enregistrée pour ce voisin, mettre à jour la distance et 
        enregistrer le sommet actuel comme son prédécesseur.
     d. Marquer le sommet actuel comme "visité".
3. Optionnel (Early Exit) : 
   - Si un sommet destination ("target") est fourni, l'algorithme peut s'arrêter 
     dès que ce sommet est marqué comme visité.
"""

class Graph:
    def __init__(self, vertices):
        """
        Initialise le graphe avec une liste de sommets.
        vertices: liste des identifiants des sommets (ex: ['A', 'B', 'C', ...])
        """
        self.vertices = vertices
        # Utilisation d'un dictionnaire d'adjacence : {sommet: {voisin: poids}}
        self.adj_list = {v: {} for v in vertices}

    def add_edge(self, u, v, weight, directed=False):
        """Ajoute une arête du sommet u au sommet v avec un poids."""
        self.adj_list[u][v] = weight
        if not directed:
            self.adj_list[v][u] = weight  # Graphe non orienté par défaut

    def dijkstra(self, source, target=None):
        """
        Exécute l'algorithme de Dijkstra depuis un sommet source.
        Peut s'arrêter prématurément si un sommet 'target' est atteint.
        
        Retourne :
        - (distances, predecessors)
        """
        distances = {v: float('inf') for v in self.vertices}
        predecessors = {v: None for v in self.vertices}
        distances[source] = 0
        visited = set()

        while len(visited) < len(self.vertices):
            # 1. Trouver le sommet non visité avec la plus petite distance
            current_vertex = None
            min_dist = float('inf')
            for v in self.vertices:
                if v not in visited and distances[v] < min_dist:
                    min_dist = distances[v]
                    current_vertex = v

            # Si tous les sommets restants sont inaccessibles, on arrête
            if current_vertex is None:
                break

            # 2. Si on a atteint la cible spécifique, on peut arrêter (Early Exit)
            if target and current_vertex == target:
                break

            # 3. Marquer comme visité
            visited.add(current_vertex)

            # 4. Relâcher les arêtes vers les voisins
            for neighbor, weight in self.adj_list[current_vertex].items():
                if neighbor not in visited:
                    new_distance = distances[current_vertex] + weight
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        predecessors[neighbor] = current_vertex

        return distances, predecessors

    def get_path(self, predecessors, start, end):
        """
        Reconstruit le chemin le plus court en utilisant le dictionnaire des prédécesseurs.
        """
        path = []
        current = end
        
        # Remonter du point d'arrivée jusqu'au point de départ
        while current is not None:
            path.insert(0, current)
            if current == start:
                break
            current = predecessors.get(current)
            
        if not path or path[0] != start:
            return "Pas de chemin"
        return "->".join(path)


# --- TESTS UNITAIRES ---

class TestDijkstra(unittest.TestCase):

    def setUp(self):
        # Initialisation d'un graphe non orienté pour les tests
        self.graph = Graph(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
        self.graph.add_edge('D', 'A', 4)
        self.graph.add_edge('D', 'E', 2)
        self.graph.add_edge('A', 'C', 3)
        self.graph.add_edge('A', 'E', 4)
        self.graph.add_edge('E', 'C', 4)
        self.graph.add_edge('E', 'G', 5)
        self.graph.add_edge('C', 'F', 5)
        self.graph.add_edge('C', 'B', 2)
        self.graph.add_edge('B', 'F', 2)
        self.graph.add_edge('G', 'F', 5)

    def test_shortest_distances_from_source(self):
        distances, preds = self.graph.dijkstra('D')
        
        # Vérification des distances minimales calculées depuis D
        self.assertEqual(distances['D'], 0)
        self.assertEqual(distances['E'], 2)
        self.assertEqual(distances['A'], 4)
        self.assertEqual(distances['C'], 6) # D -> E -> C (2 + 4) ou D -> A -> C (4 + 3) = 7. Min est 6.
        self.assertEqual(distances['G'], 7) # D -> E -> G (2 + 5)
        self.assertEqual(distances['B'], 8) # D -> E -> C -> B (2 + 4 + 2)
        self.assertEqual(distances['F'], 10) # D -> E -> C -> B -> F (2 + 4 + 2 + 2)

    def test_shortest_path_reconstruction(self):
        distances, preds = self.graph.dijkstra('D')
        
        # Vérifier la reconstruction du chemin
        path_to_F = self.graph.get_path(preds, 'D', 'F')
        self.assertEqual(path_to_F, "D->E->C->B->F")

    def test_directed_graph(self):
        # Création d'un graphe orienté simple : A -> B (2), A -> C (5), B -> C (1)
        directed_g = Graph(['A', 'B', 'C'])
        directed_g.add_edge('A', 'B', 2, directed=True)
        directed_g.add_edge('A', 'C', 5, directed=True)
        directed_g.add_edge('B', 'C', 1, directed=True)
        
        distances, preds = directed_g.dijkstra('A')
        self.assertEqual(distances['C'], 3) # A -> B -> C est plus court que A -> C
        self.assertEqual(directed_g.get_path(preds, 'A', 'C'), "A->B->C")

    def test_unreachable_node(self):
        # Ajouter un noeud déconnecté du reste
        self.graph.vertices.append('Z')
        self.graph.adj_list['Z'] = {}
        
        distances, preds = self.graph.dijkstra('D')
        self.assertEqual(distances['Z'], float('inf'))
        self.assertEqual(self.graph.get_path(preds, 'D', 'Z'), "Pas de chemin")

    def test_early_exit_with_target(self):
        # Si on s'arrête à E, les noeuds plus lointains ne devraient pas être totalement calculés
        distances, preds = self.graph.dijkstra('D', target='E')
        
        # La distance de D à E doit être correcte
        self.assertEqual(distances['E'], 2)
        # Mais un noeud éloigné comme F gardera l'infini car l'algorithme s'est arrêté tôt
        self.assertEqual(distances['F'], float('inf'))


if __name__ == '__main__':
    unittest.main()