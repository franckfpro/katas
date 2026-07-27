"""
Kata Monty Hall - Consignes

Contexte :
Le problème de Monty Hall est basé sur le jeu télévisé du même nom. Le candidat 
se retrouve face à 3 portes. Derrière l'une d'elles se trouve un prix (une voiture), 
et derrière les deux autres, des chèvres. Le candidat choisit une porte. Le 
présentateur (qui sait où se trouve le prix) révèle alors une chèvre derrière 
l'une des portes non choisies. Il offre ensuite au candidat la possibilité de 
garder son choix initial ou de changer pour la dernière porte fermée.
Le candidat a-t-il intérêt à changer ?

Instructions :
1. Écrivez un programme qui démontre s'il y a un avantage à changer de porte.
2. Votre programme doit simuler un jeu avec 3 portes et mémoriser l'emplacement du prix.
3. Il doit simuler le choix d'une porte, puis la révélation d'une mauvaise porte 
   restante par le présentateur.
4. Appliquez ensuite une stratégie : "Garder" (Stay) ou "Changer" (Switch).
5. Suivez le pourcentage de victoire de chaque stratégie.
6. Itérez le jeu 1000 fois pour comparer les deux pourcentages.

Crédit supplémentaire (Extra Credit) :
Au lieu de 3 portes, considérez un plus grand ensemble d'options, comme un jeu de 
52 cartes. Le candidat cherche l'As de Pique. Il tire une carte au hasard. Le 
présentateur révèle alors 50 autres cartes qui ne sont pas l'As de Pique. 
Le candidat a le même choix : garder sa carte ou changer pour la dernière carte 
restante. Suivez le pourcentage de victoire de chaque stratégie dans ce scénario.
"""

import random
import unittest
from unittest.mock import patch

def play_monty_hall(switch_strategy: bool, total_doors: int = 3) -> bool:
    """
    Joue une partie de Monty Hall.
    
    :param switch_strategy: True si le joueur décide de changer de porte, False sinon.
    :param total_doors: Le nombre total de portes (3 par défaut, 52 pour l'Extra Credit).
    :return: True si le joueur gagne le prix, False sinon.
    """
    doors = list(range(total_doors))
    
    # Le prix est caché derrière une porte aléatoire
    prize_door = random.choice(doors)
    
    # Le joueur choisit une porte aléatoirement
    initial_choice = random.choice(doors)
    
    # Le présentateur identifie les portes qu'il peut révéler (ni le prix, ni le choix du joueur)
    host_options = [d for d in doors if d != prize_door and d != initial_choice]
    
    # Le présentateur révèle toutes les portes sauf une parmi celles non choisies par le joueur
    # Il révèle donc (total_doors - 2) portes
    revealed_doors = set(random.sample(host_options, total_doors - 2))
    
    # Les portes restantes sont celles qui n'ont pas été révélées
    remaining_doors = [d for d in doors if d not in revealed_doors]
    
    # Application de la stratégie
    if switch_strategy:
        # Le joueur change pour l'autre porte restante
        final_choice = [d for d in remaining_doors if d != initial_choice][0]
    else:
        # Le joueur garde son choix initial
        final_choice = initial_choice
        
    return final_choice == prize_door


def simulate_games(iterations: int, switch_strategy: bool, total_doors: int = 3) -> float:
    """
    Simule plusieurs parties et retourne le taux de victoire.
    """
    wins = sum(1 for _ in range(iterations) if play_monty_hall(switch_strategy, total_doors))
    return (wins / iterations) * 100


# ==========================================
# SUITE DE TESTS UNITAIRES
# ==========================================

class TestMontyHall(unittest.TestCase):

    @patch('random.choice')
    def test_stay_strategy_wins_if_initial_choice_is_correct(self, mock_choice):
        # Configuration : le prix est en 0, le joueur choisit 0.
        mock_choice.side_effect = [0, 0] 
        # Si le joueur garde son choix, il doit gagner.
        self.assertTrue(play_monty_hall(switch_strategy=False, total_doors=3))

    @patch('random.choice')
    def test_switch_strategy_wins_if_initial_choice_is_wrong(self, mock_choice):
        # Configuration : le prix est en 0, le joueur choisit 1.
        mock_choice.side_effect = [0, 1] 
        # Si le joueur change (le présentateur révélera forcément 2), il choisira 0 et gagnera.
        self.assertTrue(play_monty_hall(switch_strategy=True, total_doors=3))

    @patch('random.choice')
    def test_switch_strategy_loses_if_initial_choice_is_correct(self, mock_choice):
        # Configuration : le prix est en 0, le joueur choisit 0.
        mock_choice.side_effect = [0, 0] 
        # Si le joueur change, il abandonne la bonne porte et doit perdre.
        self.assertFalse(play_monty_hall(switch_strategy=True, total_doors=3))

    def test_statistical_distribution_3_doors(self):
        """
        Vérifie la répartition statistique sur 10 000 parties pour 3 portes.
        Les probabilités théoriques sont : 33.33% pour Garder, 66.66% pour Changer.
        Nous utilisons un grand nombre d'itérations et un delta tolérant.
        """
        iterations = 10000
        stay_win_rate = simulate_games(iterations, switch_strategy=False, total_doors=3)
        switch_win_rate = simulate_games(iterations, switch_strategy=True, total_doors=3)
        
        self.assertAlmostEqual(stay_win_rate, 33.33, delta=2.0)
        self.assertAlmostEqual(switch_win_rate, 66.66, delta=2.0)

    def test_statistical_distribution_52_cards(self):
        """
        Vérifie la répartition statistique sur 10 000 parties pour 52 cartes (Extra Credit).
        Les probabilités théoriques sont : ~1.9% pour Garder, ~98.1% pour Changer.
        """
        iterations = 10000
        stay_win_rate = simulate_games(iterations, switch_strategy=False, total_doors=52)
        switch_win_rate = simulate_games(iterations, switch_strategy=True, total_doors=52)
        
        self.assertAlmostEqual(stay_win_rate, 1.9, delta=1.5)
        self.assertAlmostEqual(switch_win_rate, 98.1, delta=1.5)


if __name__ == '__main__':
    unittest.main()