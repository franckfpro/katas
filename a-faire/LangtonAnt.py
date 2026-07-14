import unittest

"""
KATA : LA FOURMI DE LANGTON (LANGTON ANT)

À propos de ce Kata :
L'objectif est de construire un automate cellulaire : la Fourmi de Langton.

Règles de base :
Les cases d'un plan sont colorées en noir ou en blanc. Nous identifions arbitrairement 
une case comme étant la "fourmi". La fourmi peut se déplacer dans l'une des quatre 
directions cardinales à chaque étape. Elle se déplace selon les règles suivantes :
- Sur une case blanche : tourner de 90° à droite, inverser la couleur de la case (devient noire), avancer d'une unité.
- Sur une case noire : tourner de 90° à gauche, inverser la couleur de la case (devient blanche), avancer d'une unité.

Une nouvelle couleur (Extension) :
Ajoutez la couleur rouge. La règle de changement de couleur devient une mise à jour circulaire.
Les nouvelles règles sont :
- Sur une case blanche : tourner de 90° à droite, changer la couleur de la case en noir, avancer d'une unité.
- Sur une case noire : tourner de 90° à gauche, changer la couleur de la case en rouge, avancer d'une unité.
- Sur une case rouge : ne pas tourner, changer la couleur de la case en blanc, avancer d'une unité.
"""

class LangtonAnt:
    def __init__(self, extended_rules=False):
        """
        Initialise la fourmi. 
        extended_rules: False pour les règles classiques, True pour l'extension avec le Rouge.
        """
        self.extended = extended_rules
        self.grid = {}  # Dictionnaire pour stocker l'état des cases visitées {(x, y): 'W', 'B', 'R'}
        
        # Position initiale
        self.x = 0
        self.y = 0
        
        # Direction initiale: orienté vers le Haut (0, 1)
        # Directions : Haut=(0, 1), Droite=(1, 0), Bas=(0, -1), Gauche=(-1, 0)
        self.dx = 0
        self.dy = 1

    def get_color(self):
        """Retourne la couleur de la case actuelle (Blanc par défaut)."""
        return self.grid.get((self.x, self.y), 'W')

    def turn_right(self):
        """Pivote de 90 degrés vers la droite."""
        self.dx, self.dy = self.dy, -self.dx

    def turn_left(self):
        """Pivote de 90 degrés vers la gauche."""
        self.dx, self.dy = -self.dy, self.dx

    def step(self):
        """Exécute une étape de l'automate cellulaire."""
        color = self.get_color()

        if not self.extended:
            # Règles classiques (Blanc et Noir)
            if color == 'W':
                self.turn_right()
                self.grid[(self.x, self.y)] = 'B'
            elif color == 'B':
                self.turn_left()
                self.grid[(self.x, self.y)] = 'W'
        else:
            # Nouvelles règles (Blanc, Noir, Rouge)
            if color == 'W':
                self.turn_right()
                self.grid[(self.x, self.y)] = 'B'
            elif color == 'B':
                self.turn_left()
                self.grid[(self.x, self.y)] = 'R'
            elif color == 'R':
                # Ne pas tourner
                self.grid[(self.x, self.y)] = 'W'

        # Avancer d'une unité dans la direction actuelle
        self.x += self.dx
        self.y += self.dy


# --- TESTS UNITAIRES ---

class TestLangtonAnt(unittest.TestCase):

    def test_classic_rule_on_white_square(self):
        # Sur une case blanche: tourne à droite, devient noir, avance
        ant = LangtonAnt(extended_rules=False)
        ant.step()
        
        # La case d'origine (0, 0) doit être devenue Noire ('B')
        self.assertEqual(ant.grid.get((0, 0)), 'B')
        # La fourmi pointait vers le Haut (0, 1), tourner à droite donne Droite (1, 0)
        self.assertEqual((ant.x, ant.y), (1, 0))

    def test_classic_rule_on_black_square(self):
        # Sur une case noire: tourne à gauche, devient blanc, avance
        ant = LangtonAnt(extended_rules=False)
        ant.grid[(0, 0)] = 'B' # Forcer la case de départ en Noir
        ant.step()
        
        # La case d'origine (0, 0) doit être devenue Blanche ('W')
        self.assertEqual(ant.grid.get((0, 0)), 'W')
        # La fourmi pointait vers le Haut (0, 1), tourner à gauche donne Gauche (-1, 0)
        self.assertEqual((ant.x, ant.y), (-1, 0))

    def test_extended_rule_on_white_square(self):
        # Règles étendues : case blanche identique aux règles classiques
        ant = LangtonAnt(extended_rules=True)
        ant.step()
        
        self.assertEqual(ant.grid.get((0, 0)), 'B')
        self.assertEqual((ant.x, ant.y), (1, 0))

    def test_extended_rule_on_black_square(self):
        # Règles étendues : Sur case noire: tourne à gauche, devient ROUGE, avance
        ant = LangtonAnt(extended_rules=True)
        ant.grid[(0, 0)] = 'B'
        ant.step()
        
        self.assertEqual(ant.grid.get((0, 0)), 'R')
        self.assertEqual((ant.x, ant.y), (-1, 0))

    def test_extended_rule_on_red_square(self):
        # Règles étendues : Sur case rouge: ne tourne pas, devient blanc, avance
        ant = LangtonAnt(extended_rules=True)
        ant.grid[(0, 0)] = 'R'
        ant.step()
        
        self.assertEqual(ant.grid.get((0, 0)), 'W')
        # La fourmi pointait vers le Haut (0, 1), ne tourne pas, avance vers le Haut
        self.assertEqual((ant.x, ant.y), (0, 1))

    def test_multiple_steps_classic(self):
        # Vérification d'une séquence de 2 mouvements classiques
        ant = LangtonAnt(extended_rules=False)
        ant.step() # Étape 1 : tourne à droite (1, 0), case (0, 0) devient 'B'
        ant.step() # Étape 2 : est sur (1, 0) 'W', tourne à droite (0, -1), case (1, 0) devient 'B'
        
        self.assertEqual(ant.grid.get((0, 0)), 'B')
        self.assertEqual(ant.grid.get((1, 0)), 'B')
        self.assertEqual((ant.x, ant.y), (1, -1))
        self.assertEqual((ant.dx, ant.dy), (0, -1)) # Pointe vers le bas


if __name__ == '__main__':
    unittest.main()