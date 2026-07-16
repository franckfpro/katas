import unittest

# =====================================================================
# KATA : LE JEU DE LA VIE (CONWAY'S GAME OF LIFE)
# =====================================================================
#
# CONSIGNES :
# Écrire un programme qui accepte une grille arbitraire de cellules
# et génère une grille similaire représentant la génération suivante.
# 
# Règles de gestion :
# 1. Grille finie : Dans cette version, la grille est finie et aucune
#    vie ne peut exister en dehors de ses limites (bords).
# 2. Sous-population : Toute cellule vivante ayant moins de 2 voisins vivants meurt.
# 3. Survie : Toute cellule vivante ayant 2 ou 3 voisins vivants survit.
# 4. Surpopulation : Toute cellule vivante ayant plus de 3 voisins vivants meurt.
# 5. Reproduction : Toute cellule morte ayant exactement 3 voisins vivants devient vivante.
#
# Clé du succès :
# Assurez-vous d'avoir une bonne couverture de tests pour les cas limites
# (naissances et morts sur les bords de la grille).
# =====================================================================

def prochaine_generation(grille):
    """
    Calcule la prochaine génération d'une grille du jeu de la vie.
    0 représente une cellule morte, 1 représente une cellule vivante.
    """
    if not grille or not grille[0]:
        return []

    lignes = len(grille)
    colonnes = len(grille[0])
    # Initialisation de la nouvelle grille avec des zéros
    nouvelle_grille = [[0 for _ in range(colonnes)] for _ in range(lignes)]

    def compter_voisins(r, c):
        voisins = 0
        # Les 8 directions possibles autour d'une cellule
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # On vérifie que le voisin est bien dans les limites finies de la grille
            if 0 <= nr < lignes and 0 <= nc < colonnes:
                voisins += grille[nr][nc]
        return voisins

    for r in range(lignes):
        for c in range(colonnes):
            voisins = compter_voisins(r, c)
            
            # Application des règles de Conway
            if grille[r][c] == 1:
                if voisins in (2, 3):
                    nouvelle_grille[r][c] = 1 # Survie
                else:
                    nouvelle_grille[r][c] = 0 # Mort par sous/surpopulation
            else:
                if voisins == 3:
                    nouvelle_grille[r][c] = 1 # Reproduction
                else:
                    nouvelle_grille[r][c] = 0 # Reste morte

    return nouvelle_grille


# =====================================================================
# TESTS UNITAIRES
# =====================================================================

class TestJeuDeLaVie(unittest.TestCase):

    def test_grille_vide(self):
        """Doit retourner une grille vide si on lui passe une grille vide."""
        self.assertEqual(prochaine_generation([]), [])

    def test_sous_population(self):
        """Une cellule isolée doit mourir de sous-population."""
        grille_init = [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
        attendu = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.assertEqual(prochaine_generation(grille_init), attendu)

    def test_motif_block_stable(self):
        """Un bloc de 2x2 cellules vivantes est stable (survie)."""
        grille_init = [
            [1, 1, 0],
            [1, 1, 0],
            [0, 0, 0]
        ]
        attendu = [
            [1, 1, 0],
            [1, 1, 0],
            [0, 0, 0]
        ]
        self.assertEqual(prochaine_generation(grille_init), attendu)

    def test_motif_blinker_oscillant(self):
        """Une ligne de 3 cellules pivote (oscillation simple)."""
        grille_init = [
            [0, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ]
        attendu = [
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0]
        ]
        self.assertEqual(prochaine_generation(grille_init), attendu)

    def test_reproduction_et_bords(self):
        """Test de la reproduction sur un bord (cas limite)."""
        grille_init = [
            [1, 1],
            [1, 0]
        ]
        # La cellule [1][1] a exactement 3 voisins (naissance).
        # Les autres cellules ont 2 voisins (survie).
        attendu = [
            [1, 1],
            [1, 1]
        ]
        self.assertEqual(prochaine_generation(grille_init), attendu)
        
    def test_surpopulation(self):
        """Une cellule entourée de 4 voisins doit mourir."""
        grille_init = [
            [1, 1, 1],
            [1, 1, 0],
            [0, 0, 0]
        ]
        # La cellule centrale (1,1) a 4 voisins et doit mourir.
        attendu = [
            [1, 0, 1],
            [1, 0, 1],
            [0, 0, 0]
        ]
        self.assertEqual(prochaine_generation(grille_init), attendu)

if __name__ == '__main__':
    unittest.main()