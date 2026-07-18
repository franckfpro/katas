"""
Kata Mars Rover - Consignes

Vous faites partie de l'équipe qui conçoit le Mars Rover.
Développez le programme simulateur qui prend des commandes et une carte,
traduit les commandes et affiche la position et la direction finales du Rover.

Prérequis :
Votre programme prend en entrée :
- Le point de départ du rover (x, y) et la direction (N, S, E, W) à laquelle il fait face.
- Une carte décrivant l'emplacement des obstacles.
- Une liste de commandes pour déplacer et faire tourner le rover :
  'F' (ou ⬆️) : avancer (move forward)
  'R' (ou ➡️) : tourner à droite de 90° (turn right)
  'L' (ou ⬅️) : tourner à gauche de 90° (turn left)

Règle supplémentaire :
Lorsque le rover rencontre un obstacle, il ne fait rien (le mouvement vers la case 
bloquée est ignoré, mais le rover continue de traiter les commandes suivantes).
"""

import unittest

class Rover:
    # Ordre circulaire des points cardinaux (très utile pour les rotations)
    DIRECTIONS = ['N', 'E', 'S', 'W']
    
    # Vecteurs de déplacement sur un plan cartésien standard
    MOVES = {
        'N': (0, 1),
        'E': (1, 0),
        'S': (0, -1),
        'W': (-1, 0)
    }

    def __init__(self, x, y, direction, obstacles=None):
        self.x = x
        self.y = y
        self.direction = direction
        # Utilisation d'un Set pour une recherche d'obstacle ultra-rapide
        self.obstacles = obstacles if obstacles else set()

    def execute(self, commands):
        """Prend une liste de commandes et exécute les actions correspondantes."""
        for command in commands:
            if command in ('R', '➡️'):
                self._turn_right()
            elif command in ('L', '⬅️'):
                self._turn_left()
            elif command in ('F', '⬆️'):
                self._move_forward()

    def _turn_right(self):
        current_idx = self.DIRECTIONS.index(self.direction)
        self.direction = self.DIRECTIONS[(current_idx + 1) % 4]

    def _turn_left(self):
        current_idx = self.DIRECTIONS.index(self.direction)
        self.direction = self.DIRECTIONS[(current_idx - 1) % 4]

    def _move_forward(self):
        dx, dy = self.MOVES[self.direction]
        next_x, next_y = self.x + dx, self.y + dy
        
        # Vérification anti-collision avec la carte des obstacles
        if (next_x, next_y) not in self.obstacles:
            self.x, self.y = next_x, next_y
        # Si un obstacle est présent, le rover "ne fait rien" et reste sur place

    def get_position(self):
        return self.x, self.y, self.direction


# ==========================================
# SUITE DE TESTS UNITAIRES
# ==========================================

class TestMarsRover(unittest.TestCase):
    
    def test_initial_position(self):
        rover = Rover(0, 0, 'N')
        self.assertEqual(rover.get_position(), (0, 0, 'N'))

    def test_turn_right(self):
        rover = Rover(0, 0, 'N')
        
        # Test avec lettre
        rover.execute(['R'])
        self.assertEqual(rover.get_position(), (0, 0, 'E'))
        
        # Test avec emoji
        rover.execute(['➡️'])
        self.assertEqual(rover.get_position(), (0, 0, 'S'))

    def test_turn_left(self):
        rover = Rover(0, 0, 'N')
        
        # Test avec lettre
        rover.execute(['L'])
        self.assertEqual(rover.get_position(), (0, 0, 'W'))
        
        # Test avec emoji
        rover.execute(['⬅️'])
        self.assertEqual(rover.get_position(), (0, 0, 'S'))

    def test_move_forward(self):
        rover = Rover(0, 0, 'N')
        rover.execute(['F', 'F'])
        self.assertEqual(rover.get_position(), (0, 2, 'N'))

    def test_complex_path(self):
        rover = Rover(1, 2, 'E')
        # Avance de 2 cases -> (3, 2)
        # Tourne à gauche -> face au N
        # Avance de 1 case -> (3, 3)
        rover.execute(['F', 'F', 'L', 'F'])
        self.assertEqual(rover.get_position(), (3, 3, 'N'))

    def test_obstacle_avoidance(self):
        # On place un obstacle exactement devant le rover
        obstacles = {(0, 1)}
        rover = Rover(0, 0, 'N', obstacles)
        
        # Le rover tente d'avancer (bloqué), puis tourne à droite, puis avance.
        rover.execute(['F', 'R', 'F'])
        
        # Le premier 'F' a été ignoré, le rover était donc en (0,0).
        # Il a tourné vers l'Est, puis avancé, atterrissant en (1,0).
        self.assertEqual(rover.get_position(), (1, 0, 'E'))


if __name__ == '__main__':
    unittest.main()