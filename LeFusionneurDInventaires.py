"""
KATA PYTHON #044 - Le Fusionneur d'Inventaires
Difficulté : 4/10

ÉNONCÉ :
Dans le cadre d'un jeu vidéo RPG, vous devez fusionner l'inventaire actuel du 
joueur avec le contenu d'un coffre qu'il vient de trouver.

Chaque inventaire est représenté par un dictionnaire où :
- La clé (str) est le nom de l'objet (ex: "potion").
- La valeur (dict) contient les détails de l'objet, à savoir sa "quantite" (int)
  et sa "rarete" (str : "commun", "rare", "épique").

On vous demande de compléter la fonction `fusionner_inventaires`.

RÈGLES ET CONTRAINTES :
1. Si un objet est présent dans les deux inventaires, ses quantités s'additionnent.
2. Si un objet a la même clé mais deux raretés différentes (ex: "épée" commune dans 
   le coffre et "épée" rare sur le joueur), vous devez conserver uniquement la version 
   ayant la rareté la plus élevée selon l'ordre : "commun" < "rare" < "épique".
   La quantité finale sera alors uniquement celle de l'objet qui a gagné le duel de rareté.
3. Si un objet n'est que dans un seul inventaire, il est simplement ajouté au résultat.
4. La fonction ne doit pas modifier les dictionnaires d'origine passés en paramètre 
   (effet de bord interdit).

Exemple :
joueur = {"potion": {"quantite": 2, "rarete": "commun"}}
coffre = {"potion": {"quantite": 5, "rarete": "commun"}, "épée": {"quantite": 1, "rarete": "rare"}}

Résultat attendu :
{
    "potion": {"quantite": 7, "rarete": "commun"},
    "épée": {"quantite": 1, "rarete": "rare"}
}
"""

import copy
import unittest


def fusionner_inventaires(joueur: dict, coffre: dict) -> dict:
    """Fusionne l'inventaire du joueur et du coffre selon les règles de rareté

    et de quantité. Retourne un nouveau dictionnaire.
    """
    # TODO: Implémenter la logique ici
    pass


# =====================================================================
# TESTS UNITAIRES (Ne pas modifier cette section)
# =====================================================================

class TestFusionInventaire(unittest.TestCase):
    """Suite de tests pour valider votre fonction fusionner_inventaires."""

    def setUp(self):
        """Initialisation des inventaires de test."""
        self.inv_joueur = {
            "potion": {"quantite": 3, "rarete": "commun"},
            "bouclier": {"quantite": 1, "rarete": "rare"},
            "epee": {"quantite": 1, "rarete": "commun"}
        }
        self.inv_coffre = {
            "potion": {"quantite": 2, "rarete": "commun"},
            "epee": {"quantite": 1, "rarete": "epique"},
            "or": {"quantite": 100, "rarete": "commun"}
        }

    def test_fusion_simple_et_addition(self):
        """Vérifie l'addition des quantités pour des raretés identiques (potion)"""
        # On copie pour éviter les effets de bord entre les tests
        j = copy.deepcopy(self.inv_joueur)
        c = {"potion": {"quantite": 5, "rarete": "commun"}}
        
        resultat = fusionner_inventaires(j, c)
        self.assertEqual(resultat["potion"]["quantite"], 8)
        self.assertEqual(resultat["potion"]["rarete"], "commun")

    def test_conflit_rarete_gagne_coffre(self):
        """L'épée épique du coffre doit remplacer l'épée commune du joueur."""
        resultat = fusionner_inventaires(self.inv_joueur, self.inv_coffre)
        
        # L'épée épique écrase la commune, sa quantité devient 1 (celle du coffre)
        self.assertEqual(resultat["epee"]["rarete"], "epique")
        self.assertEqual(resultat["epee"]["quantite"], 1)

    def test_conflit_rarete_gagne_joueur(self):
        """L'objet du joueur doit rester si sa rareté est supérieure."""
        j = {"arc": {"quantite": 1, "rarete": "epique"}}
        c = {"arc": {"quantite": 3, "rarete": "rare"}}
        
        resultat = fusionner_inventaires(j, c)
        self.assertEqual(resultat["arc"]["rarete"], "epique")
        self.assertEqual(resultat["arc"]["quantite"], 1)

    def test_objets_uniques(self):
        """Les objets présents uniquement d'un côté doivent être conservés."""
        resultat = fusionner_inventaires(self.inv_joueur, self.inv_coffre)
        
        self.assertIn("bouclier", resultat)
        self.assertIn("or", resultat)
        self.assertEqual(resultat["or"]["quantite"], 100)

    def test_pas_d_effet_de_bord(self):
        """La fonction ne doit absolument pas modifier les dictionnaires parents."""
        j_copie = copy.deepcopy(self.inv_joueur)
        c_copie = copy.deepcopy(self.inv_coffre)
        
        _ = fusionner_inventaires(self.inv_joueur, self.inv_coffre)
        
        self.assertEqual(self.inv_joueur, j_copie)
        self.assertEqual(self.inv_coffre, c_copie)


if __name__ == "__main__":
    unittest.main(verbosity=2)