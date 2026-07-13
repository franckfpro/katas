import unittest

"""
KATA GREED (JEU DE DÉS)

Description du problème :
Écrivez une méthode qui évalue et calcule le meilleur score basé sur un lancer 
de dés (sous forme de liste d'entiers), en respectant les règles du jeu Greed.

Règles de base :
- Un 1 vaut 100 points.
- Un 5 vaut 50 points.
- Brelan de 1 (trois '1') = 1000 points.
- Brelan de 2 (trois '2') = 200 points.
- Brelan de 3 (trois '3') = 300 points.
- Brelan de 4 (trois '4') = 400 points.
- Brelan de 5 (trois '5') = 500 points.
- Brelan de 6 (trois '6') = 600 points.

Note : Les dés de la liste ne peuvent être marqués qu'une seule fois.

--- BONUS (POUR ALLER PLUS LOIN) ---
Modifiez votre méthode pour supporter jusqu'à 6 dés et ces règles supplémentaires :
- Carré (quatre dés identiques) : Multiplie le score du brelan par 2 (ex: quatre '2' = 400).
- Quintuple (cinq dés) : Multiplie le score du brelan par 4.
- Sextuple (six dés) : Multiplie le score du brelan par 8.
- Trois paires (ex: 2, 2, 3, 3, 4, 4) : 800 points.
- Suite (1, 2, 3, 4, 5, 6) : 1200 points.
"""

def calculer_score(des: list[int]) -> int:
    """
    Calcule le score d'un lancer de dés selon les règles standards de Greed.
    """
    if not des:
        return 0
        
    # Compter l'occurrence de chaque face (de 1 à 6)
    occurrences = {i: des.count(i) for i in range(1, 7)}
    score_total = 0

    for face, quantite in occurrences.items():
        # Déterminer combien de brelans (groupes de 3) et de dés restants (isolés)
        brelans = quantite // 3
        des_isoles = quantite % 3

        # Calcul des points pour les brelans
        if brelans > 0:
            if face == 1:
                score_total += brelans * 1000
            else:
                score_total += brelans * face * 100

        # Calcul des points pour les dés isolés restants
        if face == 1:
            score_total += des_isoles * 100
        elif face == 5:
            score_total += des_isoles * 50

    return score_total


# --- TESTS UNITAIRES ---

class TestGreed(unittest.TestCase):
    
    def test_lancer_vide(self):
        """Un lancer sans aucun dé rapporte 0 point."""
        self.assertEqual(calculer_score([]), 0)

    def test_lancer_sans_point(self):
        """Test d'un lancer qui ne marque aucun point [2, 3, 4, 6, 2]."""
        self.assertEqual(calculer_score([2, 3, 4, 6, 2]), 0)

    def test_des_isoles_uniquement(self):
        """Test uniquement des 1 et des 5 isolés."""
        self.assertEqual(calculer_score([1]), 100)
        self.assertEqual(calculer_score([5]), 50)
        self.assertEqual(calculer_score([1, 5, 1]), 250)

    def test_brelan_de_un(self):
        """Test d'un brelan de 1, qui est une exception valant 1000 points."""
        self.assertEqual(calculer_score([1, 1, 1]), 1000)

    def test_autres_brelans(self):
        """Test de la règle générique pour les autres brelans (face * 100)."""
        self.assertEqual(calculer_score([2, 2, 2]), 200)
        self.assertEqual(calculer_score([3, 3, 3]), 300)
        self.assertEqual(calculer_score([4, 4, 4]), 400)
        self.assertEqual(calculer_score([5, 5, 5]), 500)
        self.assertEqual(calculer_score([6, 6, 6]), 600)

    def test_combinaison_brelan_et_isoles(self):
        """Test l'exemple principal donné dans les instructions [1, 1, 1, 5, 1]."""
        # Brelan de 1 (1000) + 1 isolé (100) + 5 isolé (50) = 1150
        self.assertEqual(calculer_score([1, 1, 1, 5, 1]), 1150)

    def test_combinaison_brelan_sans_valeur_isolee_pour_le_reste(self):
        """Test d'un lancer mixte [3, 4, 5, 3, 3]."""
        # Brelan de 3 (300) + 5 isolé (50) + 4 isolé (0) = 350
        self.assertEqual(calculer_score([3, 4, 5, 3, 3]), 350)

    # -------------------------------------------------------------------------
    # DÉFI "EXTRA CREDIT" :
    # Dé-commentez ces tests un par un pour étendre votre fonction et
    # implémenter les règles bonus.
    # -------------------------------------------------------------------------

    # def test_carre_multiplie_brelan_par_2(self):
    #     """4 dés identiques : Multiplie le score du brelan par 2."""
    #     self.assertEqual(calculer_score([2, 2, 2, 2]), 400)
    #     self.assertEqual(calculer_score([1, 1, 1, 1]), 2000)
    #
    # def test_quintuple_multiplie_brelan_par_4(self):
    #     """5 dés identiques : Multiplie le score du brelan par 4."""
    #     self.assertEqual(calculer_score([2, 2, 2, 2, 2]), 800)
    #
    # def test_sextuple_multiplie_brelan_par_8(self):
    #     """6 dés identiques : Multiplie le score du brelan par 8."""
    #     self.assertEqual(calculer_score([2, 2, 2, 2, 2, 2]), 1600)
    #
    # def test_trois_paires(self):
    #     """Une combinaison exacte de trois paires vaut 800 points."""
    #     self.assertEqual(calculer_score([2, 2, 3, 3, 4, 4]), 800)
    #
    # def test_suite_complete(self):
    #     """Une suite de 1 à 6 vaut 1200 points."""
    #     self.assertEqual(calculer_score([1, 2, 3, 4, 5, 6]), 1200)


if __name__ == '__main__':
    unittest.main()