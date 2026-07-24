"""
Kata Démineur (Minesweeper) - Consignes

Avez-vous déjà joué au Démineur ? Le but du jeu est de trouver toutes les mines 
dans un champ de M x N cases. Pour vous aider, le jeu affiche un nombre dans 
chaque case vide qui vous indique combien de mines lui sont adjacentes.

Par exemple, prenez le champ 4x4 suivant contenant 2 mines (représentées par un '*') :
*...
....
.*..
....

Le même champ incluant les nombres indices décrits ci-dessus ressemblerait à ceci :
*100
2210
1*10
1110

Objectif :
Vous devez écrire une fonction qui prend en entrée un champ (une liste de chaînes 
de caractères représentant les lignes), où chaque case sûre est représentée par 
un '.' et chaque mine par un '*'. La fonction doit retourner le champ résolu où 
les '.' sont remplacés par le nombre de mines adjacentes à cette case (de 0 à 8).
"""

import unittest

def solve_minesweeper(grid):
    """
    Calcule le nombre de mines adjacentes pour chaque case vide d'une grille de démineur.
    
    :param grid: list[str] représentant la grille de départ.
    :return: list[str] représentant la grille résolue.
    """
    if not grid:
        return []

    rows = len(grid)
    cols = len(grid[0])
    solved_grid = []

    for r in range(rows):
        current_row = ""
        for c in range(cols):
            # Si la case est une mine, on la conserve telle quelle
            if grid[r][c] == '*':
                current_row += '*'
            else:
                # Sinon, on compte les mines dans les 8 cases adjacentes
                mine_count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        # On ignore la case centrale (elle-même)
                        if dr == 0 and dc == 0:
                            continue
                        
                        nr, nc = r + dr, c + dc
                        
                        # Vérification des limites de la grille
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if grid[nr][nc] == '*':
                                mine_count += 1
                
                current_row += str(mine_count)
        solved_grid.append(current_row)

    return solved_grid


# ==========================================
# SUITE DE TESTS UNITAIRES
# ==========================================

class TestMinesweeper(unittest.TestCase):
    
    def test_example_4x4(self):
        grid = [
            "*...",
            "....",
            ".*..",
            "...."
        ]
        expected = [
            "*100",
            "2210",
            "1*10",
            "1110"
        ]
        self.assertEqual(solve_minesweeper(grid), expected)

    def test_example_3x5(self):
        grid = [
            "**...",
            ".....",
            ".*..."
        ]
        expected = [
            "**100",
            "33200",
            "1*100"
        ]
        self.assertEqual(solve_minesweeper(grid), expected)

    def test_empty_grid(self):
        self.assertEqual(solve_minesweeper([]), [])

    def test_all_mines(self):
        grid = [
            "**",
            "**"
        ]
        expected = [
            "**",
            "**"
        ]
        self.assertEqual(solve_minesweeper(grid), expected)

    def test_no_mines(self):
        grid = [
            "...",
            "..."
        ]
        expected = [
            "000",
            "000"
        ]
        self.assertEqual(solve_minesweeper(grid), expected)

    def test_single_row(self):
        grid = ["*..*."]
        expected = ["*11*1"]
        self.assertEqual(solve_minesweeper(grid), expected)

    def test_single_column(self):
        grid = [
            "*",
            ".",
            ".",
            "*"
        ]
        expected = [
            "*",
            "1",
            "1",
            "*"
        ]
        self.assertEqual(solve_minesweeper(grid), expected)


if __name__ == '__main__':
    unittest.main()