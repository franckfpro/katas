"""
======================================================================
KATA : ZOMBIE SURVIVORS
======================================================================

CONSIGNES (Itérations 1 à 3) :

Étape 1 : Les Survivants
L'apocalypse zombie a eu lieu. Vous devez modéliser un Survivant.
- Chaque Survivant a un Nom.
- Chaque Survivant commence avec 0 Blessure (Wound).
- Un Survivant qui reçoit 2 Blessures meurt immédiatement ; les 
  blessures supplémentaires sont ignorées.
- Chaque Survivant commence avec la capacité d'effectuer 3 Actions par tour.

Étape 2 : L'Équipement
Les Survivants peuvent utiliser de l'équipement pour s'aider.
- Chaque Survivant peut transporter jusqu'à 5 pièces d'Équipement.
- Chaque Blessure reçue par un Survivant réduit de 1 le nombre de 
  pièces d'Équipement qu'il peut transporter.
- Si le Survivant a plus d'Équipement que sa nouvelle capacité, 
  il doit se défausser d'une pièce (implémentez la logique de votre choix).

Étape 3 : Le Jeu (Game)
Un Jeu comprend un ou plusieurs Survivants.
- Un Jeu commence avec 0 Survivant.
- Un Jeu permet d'ajouter des Survivants à tout moment.
- Les Noms des Survivants dans un Jeu doivent être uniques.
- Un Jeu se termine immédiatement si tous ses Survivants sont morts.

======================================================================
"""

import unittest

# --- CODE MÉTIER ---

class Survivor:
    def __init__(self, name: str):
        self.name = name
        self.wounds = 0
        self.actions_per_turn = 3
        self.equipment = []
        
    @property
    def is_dead(self) -> bool:
        return self.wounds >= 2

    @property
    def max_equipment_capacity(self) -> int:
        return max(0, 5 - self.wounds)

    def take_wound(self):
        """Ajoute une blessure au survivant et ajuste son équipement."""
        if not self.is_dead:
            self.wounds += 1
            self._drop_excess_equipment()

    def pickup_equipment(self, item: str) -> bool:
        """Ajoute un équipement si la capacité le permet."""
        if len(self.equipment) < self.max_equipment_capacity:
            self.equipment.append(item)
            return True
        return False

    def _drop_excess_equipment(self):
        """Défausse les équipements en trop (les derniers ajoutés)."""
        while len(self.equipment) > self.max_equipment_capacity:
            self.equipment.pop()


class Game:
    def __init__(self):
        self.survivors = {}

    def add_survivor(self, survivor: Survivor):
        """Ajoute un survivant au jeu s'il a un nom unique."""
        if survivor.name in self.survivors:
            raise ValueError(f"Le nom '{survivor.name}' est déjà utilisé dans ce jeu.")
        self.survivors[survivor.name] = survivor

    @property
    def is_over(self) -> bool:
        """Le jeu est terminé si tous les survivants sont morts ou s'il n'y en a aucun."""
        if not self.survivors:
            return False
        
        # Vérifie si tous les survivants sont morts
        for survivor in self.survivors.values():
            if not survivor.is_dead:
                return False
        return True


# ======================================================================
# ZONE DE TESTS UNITAIRES
# ======================================================================
class TestZombieSurvivors(unittest.TestCase):

    # --- Tests Étape 1 : Survivants ---
    def test_survivor_starts_with_correct_defaults(self):
        survivor = Survivor("Rick")
        self.assertEqual(survivor.name, "Rick")
        self.assertEqual(survivor.wounds, 0)
        self.assertEqual(survivor.actions_per_turn, 3)
        self.assertFalse(survivor.is_dead)

    def test_survivor_dies_after_two_wounds(self):
        survivor = Survivor("Glenn")
        survivor.take_wound()
        self.assertFalse(survivor.is_dead)
        survivor.take_wound()
        self.assertTrue(survivor.is_dead)

    def test_survivor_ignores_additional_wounds_after_death(self):
        survivor = Survivor("Maggie")
        survivor.take_wound()
        survivor.take_wound()
        survivor.take_wound()
        self.assertEqual(survivor.wounds, 2)

    # --- Tests Étape 2 : Équipement ---
    def test_survivor_can_carry_up_to_five_equipments(self):
        survivor = Survivor("Michonne")
        for i in range(5):
            self.assertTrue(survivor.pickup_equipment(f"Item {i}"))
        
        # Le 6ème équipement doit être refusé
        self.assertFalse(survivor.pickup_equipment("Item 6"))
        self.assertEqual(len(survivor.equipment), 5)

    def test_wounds_reduce_equipment_capacity_and_drop_excess(self):
        survivor = Survivor("Daryl")
        survivor.pickup_equipment("Crossbow")
        survivor.pickup_equipment("Knife")
        survivor.pickup_equipment("Water")
        survivor.pickup_equipment("Food")
        survivor.pickup_equipment("Bandage")
        
        # Première blessure : capacité tombe à 4
        survivor.take_wound()
        self.assertEqual(len(survivor.equipment), 4)
        self.assertNotIn("Bandage", survivor.equipment)

    # --- Tests Étape 3 : Le Jeu ---
    def test_game_adds_survivors_with_unique_names(self):
        game = Game()
        game.add_survivor(Survivor("Carol"))
        
        with self.assertRaises(ValueError):
            game.add_survivor(Survivor("Carol"))

    def test_game_ends_when_all_survivors_are_dead(self):
        game = Game()
        rick = Survivor("Rick")
        carl = Survivor("Carl")
        
        game.add_survivor(rick)
        game.add_survivor(carl)
        
        self.assertFalse(game.is_over)
        
        rick.take_wound()
        rick.take_wound()
        self.assertFalse(game.is_over)
        
        carl.take_wound()
        carl.take_wound()
        self.assertTrue(game.is_over)


if __name__ == '__main__':
    unittest.main()