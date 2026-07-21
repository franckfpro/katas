import unittest
from typing import Set, Optional, Callable

# =============================================================================
# KATA : SUDOKU - LE RÉSOLVEUR CONCURRENT
# =============================================================================
#
# CONSIGNES :
# Ce kata explore la programmation concurrente et le TDD. Le but est de
# résoudre un Sudoku non pas par un algorithme centralisé, mais par la 
# collaboration de composants indépendants qui communiquent par messages.
#
# 1. Spécification de la Cellule (Cell) :
#    - Exprime quels nombres de 1 à 9 sont possibles. Par défaut, tous (1..9).
#    - Si > 1 nombre possible : la valeur est "inconnue" (unknown).
#    - Si 1 seul nombre possible : la valeur est "connue" (known).
#    - Si 0 nombre possible : c'est une "contradiction" (impossible).
#    - Peut répondre à : "Quelle est la valeur ?" et "X est-il possible ?".
#    - Peut enregistrer l'information : "X n'est plus une valeur possible".
#
# 2. Spécification de la Grille (Grid) :
#    - Possède un nom : A, B, C, D, E, F, G, H ou I.
#    - Contient 3x3 Cellules adressées par (Ligne, Colonne).
#    - Si une Cellule découvre sa valeur, la Grille s'assure qu'aucune 
#      autre cellule de cette grille ne peut avoir la même valeur.
#
# 3. Spécification de la Région (Region) - (Pour l'étape suivante) :
#    - Contient une Grille.
#    - Possède 4 entrées/sorties : Nord, Est, Sud, Ouest.
#    - Communique avec les autres régions via un système de messages 
#      pour s'avertir des valeurs trouvées sur les lignes/colonnes globales.
# =============================================================================


class Cell:
    """Représente une cellule unique du Sudoku."""
    
    def __init__(self):
        self._possibilities: Set[int] = set(range(1, 10))
        # Callback optionnel pour avertir la grille quand la cellule trouve sa valeur
        self.on_value_found: Optional[Callable[[int], None]] = None
        self._notified = False

    @property
    def value(self) -> str:
        """Retourne l'état actuel de la cellule."""
        if len(self._possibilities) > 1:
            return "unknown"
        elif len(self._possibilities) == 1:
            return str(next(iter(self._possibilities)))
        else:
            return "impossible"

    def is_possible(self, x: int) -> bool:
        """Vérifie si le nombre X est toujours une option valide."""
        return x in self._possibilities

    def remove_possibility(self, x: int) -> None:
        """Enregistre l'information que X n'est plus possible."""
        if x in self._possibilities:
            self._possibilities.remove(x)
            self._check_if_found()

    def _check_if_found(self):
        """Déclenche le callback si la valeur vient d'être découverte."""
        if len(self._possibilities) == 1 and not self._notified:
            self._notified = True
            if self.on_value_found:
                self.on_value_found(next(iter(self._possibilities)))


class Grid:
    """Représente une sous-grille de 3x3 cellules (Région A à I)."""
    
    def __init__(self, name: str):
        self.name = name
        # Initialisation d'une matrice 3x3 de Cellules
        self.cells = [[Cell() for _ in range(3)] for _ in range(3)]
        
        # Abonnement de la grille aux découvertes de ses propres cellules
        for r in range(3):
            for c in range(3):
                # On utilise les valeurs par défaut de r et c pour capturer l'état dans la lambda
                self.cells[r][c].on_value_found = lambda val, row=r, col=c: self._handle_cell_found(row, col, val)

    def get_cell(self, row: int, col: int) -> Cell:
        """Récupère une cellule via ses coordonnées locales (0-2, 0-2)."""
        return self.cells[row][col]

    def _handle_cell_found(self, source_row: int, source_col: int, value: int):
        """
        Quand une cellule trouve sa valeur, cette valeur devient impossible 
        pour toutes les autres cellules de cette grille 3x3.
        """
        for r in range(3):
            for c in range(3):
                if r != source_row or c != source_col:
                    self.cells[r][c].remove_possibility(value)


# =============================================================================
# TESTS UNITAIRES
# =============================================================================

class TestSudokuConcurrent(unittest.TestCase):

    def test_cell_initialization(self):
        """Une cellule nouvellement créée doit avoir toutes les possibilités (1-9) et être inconnue."""
        cell = Cell()
        self.assertEqual(cell.value, "unknown")
        for i in range(1, 10):
            self.assertTrue(cell.is_possible(i))

    def test_cell_value_discovery(self):
        """Si on retire toutes les possibilités sauf une, la cellule doit avoir une valeur connue."""
        cell = Cell()
        for i in range(1, 9): # On retire 1 à 8
            cell.remove_possibility(i)
            
        self.assertEqual(cell.value, "9")
        self.assertFalse(cell.is_possible(1))
        self.assertTrue(cell.is_possible(9))

    def test_cell_contradiction(self):
        """Si on retire toutes les possibilités, la cellule doit être en état 'impossible'."""
        cell = Cell()
        for i in range(1, 10):
            cell.remove_possibility(i)
            
        self.assertEqual(cell.value, "impossible")

    def test_grid_internal_resolution(self):
        """
        Lorsqu'une cellule d'une grille 3x3 trouve sa valeur, 
        cette valeur doit être retirée des possibilités des autres cellules de la grille.
        """
        grid = Grid("A")
        target_cell = grid.get_cell(1, 1)
        
        # On force la cellule (1,1) à devenir '5' en retirant les autres
        for i in [1, 2, 3, 4, 6, 7, 8, 9]:
            target_cell.remove_possibility(i)
            
        self.assertEqual(target_cell.value, "5")
        
        # Vérification qu'une autre cellule de la même grille ne peut plus être '5'
        sibling_cell = grid.get_cell(0, 0)
        self.assertFalse(sibling_cell.is_possible(5))
        self.assertEqual(sibling_cell.value, "unknown") # Reste inconnue car elle a encore 8 possibilités


if __name__ == '__main__':
    unittest.main()