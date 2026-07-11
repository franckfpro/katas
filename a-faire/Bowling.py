import unittest

"""
KATA BOWLING

Description du problème :
Créez un programme qui, à partir d'une séquence valide de lancers pour une partie 
de bowling américain à 10 quilles, calcule le score total de la partie.

Règles de calcul :
- Une partie comprend 10 carreaux (frames).
- Le joueur a droit à 2 lancers maximum par carreau pour faire tomber 10 quilles.
- Spare : 10 quilles tombées en 2 lancers. Bonus = valeur du prochain lancer.
- Strike : 10 quilles tombées au 1er lancer. Bonus = valeur des 2 prochains lancers.
- Au 10ème carreau, un joueur qui fait un spare ou un strike obtient des lancers bonus.

Instructions pour le Kata :
Implémentez une classe `JeuDeBowling` avec deux méthodes :
1. `lancer(quilles: int)` : appelée à chaque fois que le joueur lance une boule.
2. `score() -> int` : appelée à la fin de la partie pour calculer le score total.
"""

class JeuDeBowling:
    def __init__(self):
        self.lancers = []

    def lancer(self, quilles: int):
        """Enregistre le nombre de quilles abattues lors d'un lancer."""
        self.lancers.append(quilles)

    def score(self) -> int:
        """Calcule le score total de la partie."""
        total = 0
        index_lancer = 0
        
        for _ in range(10):
            if self._est_un_strike(index_lancer):
                total += 10 + self._bonus_strike(index_lancer)
                index_lancer += 1 # Un strike ne consomme qu'un seul lancer
            elif self._est_un_spare(index_lancer):
                total += 10 + self._bonus_spare(index_lancer)
                index_lancer += 2
            else:
                total += self._somme_quilles_carreau(index_lancer)
                index_lancer += 2
                
        return total

    # --- Méthodes privées d'aide pour rendre le code plus lisible ---

    def _est_un_strike(self, index_lancer: int) -> bool:
        return self.lancers[index_lancer] == 10

    def _est_un_spare(self, index_lancer: int) -> bool:
        return self.lancers[index_lancer] + self.lancers[index_lancer + 1] == 10

    def _bonus_strike(self, index_lancer: int) -> int:
        return self.lancers[index_lancer + 1] + self.lancers[index_lancer + 2]

    def _bonus_spare(self, index_lancer: int) -> int:
        return self.lancers[index_lancer + 2]

    def _somme_quilles_carreau(self, index_lancer: int) -> int:
        return self.lancers[index_lancer] + self.lancers[index_lancer + 1]


class TestJeuDeBowling(unittest.TestCase):
    
    def setUp(self):
        """Initialise une nouvelle partie avant chaque test."""
        self.jeu = JeuDeBowling()

    def lancer_plusieurs(self, nombre_de_lancers: int, quilles: int):
        """Fonction utilitaire pour éviter la répétition dans les tests."""
        for _ in range(nombre_de_lancers):
            self.jeu.lancer(quilles)

    def test_partie_gouttiere(self):
        """Toutes les boules tombent dans la gouttière (0 quille)."""
        self.lancer_plusieurs(20, 0)
        self.assertEqual(self.jeu.score(), 0)

    def test_partie_que_des_uns(self):
        """Une quille abattue à chaque lancer."""
        self.lancer_plusieurs(20, 1)
        self.assertEqual(self.jeu.score(), 20)

    def test_un_spare(self):
        """Test avec un seul spare au début, suivi d'un lancer à 3, puis des zéros."""
        self.jeu.lancer(5)
        self.jeu.lancer(5) # Spare
        self.jeu.lancer(3)
        self.lancer_plusieurs(17, 0)
        self.assertEqual(self.jeu.score(), 16) # 10 + 3 (bonus spare) + 3 = 16

    def test_un_strike(self):
        """Test avec un seul strike au début, suivi d'un 3 et d'un 4, puis des zéros."""
        self.jeu.lancer(10) # Strike
        self.jeu.lancer(3)
        self.jeu.lancer(4)
        self.lancer_plusieurs(16, 0)
        self.assertEqual(self.jeu.score(), 24) # 10 + 7 (bonus strike) + 7 = 24

    def test_partie_parfaite(self):
        """Test avec 12 strikes consécutifs."""
        self.lancer_plusieurs(12, 10)
        self.assertEqual(self.jeu.score(), 300)


if __name__ == '__main__':
    unittest.main()