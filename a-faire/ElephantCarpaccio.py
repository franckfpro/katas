import unittest

"""
KATA ELEPHANT CARPACCIO

Description du problème :
Développer une caisse enregistreuse capable d'émettre un ticket de caisse.
La fonction principale doit prendre 4 paramètres : 
1. Le libellé du produit (chaine de caractères)
2. La quantité (entier)
3. Le prix unitaire (décimal)
4. Le code d'état américain (2 lettres)

Le calcul s'effectue dans l'ordre suivant :
1. Calcul du montant Total Hors Taxe (HT) = Quantité * Prix Unitaire
2. Calcul et déduction de la réduction selon le montant Total HT
3. Calcul et ajout de la TVA locale en fonction de l'État sur le montant HT remisé.
"""

class CaisseEnregistreuse:
    # Dictionnaire des taux de TVA par État (exprimés en format décimal)
    TAXES_ETATS = {
        'UT': 0.0685,
        'NV': 0.08,
        'TX': 0.0625,
        'AL': 0.04,
        'CA': 0.0825
    }

    @staticmethod
    def calculer_taux_reduction(total_ht: float) -> float:
        """Détermine le taux de réduction à appliquer en fonction du Total HT."""
        if total_ht >= 50000:
            return 0.15
        elif total_ht >= 10000:
            return 0.10
        elif total_ht >= 7000:
            return 0.07
        elif total_ht >= 5000:
            return 0.05
        elif total_ht >= 1000:
            return 0.03
        return 0.0

    @classmethod
    def generer_ticket(cls, libelle: str, quantite: int, prix_unitaire: float, code_etat: str) -> dict:
        """
        Calcule les informations du ticket de caisse et retourne un dictionnaire 
        contenant le détail de la transaction.
        """
        code_etat = code_etat.upper()
        if code_etat not in cls.TAXES_ETATS:
            raise ValueError(f"Le code d'état fourni est inconnu : '{code_etat}'")

        # 1. Calcul du Total HT
        total_ht = quantite * prix_unitaire

        # 2. Application de la réduction
        taux_reduction = cls.calculer_taux_reduction(total_ht)
        montant_reduction = total_ht * taux_reduction
        total_ht_remise = total_ht - montant_reduction
        
        # 3. Application de la TVA
        taux_tva = cls.TAXES_ETATS[code_etat]
        montant_tva = total_ht_remise * taux_tva
        total_ttc = total_ht_remise + montant_tva

        return {
            "libelle": libelle,
            "quantite": quantite,
            "prix_unitaire": prix_unitaire,
            "etat": code_etat,
            "total_ht": round(total_ht, 2),
            "taux_reduction": taux_reduction,
            "montant_reduction": round(montant_reduction, 2),
            "total_ht_remise": round(total_ht_remise, 2),
            "taux_tva": taux_tva,
            "montant_tva": round(montant_tva, 2),
            "total_ttc": round(total_ttc, 2)
        }


# --- TESTS UNITAIRES ---

class TestCaisseEnregistreuse(unittest.TestCase):
    
    def test_calcul_basique_sans_reduction(self):
        """Test un achat classique (Total HT = 100), sans réduction, au Texas (TVA 6.25%)."""
        ticket = CaisseEnregistreuse.generer_ticket("Clavier", 1, 100.0, "TX")
        self.assertEqual(ticket["total_ht"], 100.0)
        self.assertEqual(ticket["taux_reduction"], 0.0)
        self.assertEqual(ticket["montant_tva"], 6.25)
        self.assertEqual(ticket["total_ttc"], 106.25)

    def test_reduction_3_pourcents(self):
        """Test le palier de réduction > 1000 (3%) dans l'Alabama (TVA 4.00%)."""
        ticket = CaisseEnregistreuse.generer_ticket("PC Portable", 1, 1000.0, "AL")
        self.assertEqual(ticket["total_ht"], 1000.0)
        self.assertEqual(ticket["taux_reduction"], 0.03)
        self.assertEqual(ticket["montant_reduction"], 30.0)
        self.assertEqual(ticket["total_ht_remise"], 970.0)
        # TVA de 4% sur 970 = 38.8
        self.assertEqual(ticket["total_ttc"], 1008.8)

    def test_reduction_15_pourcents_avec_quantite(self):
        """Test le plus haut palier > 50000 (15%) en Californie (TVA 8.25%)."""
        # 10 serveurs à 6000$ = 60000 HT
        ticket = CaisseEnregistreuse.generer_ticket("Serveur", 10, 6000.0, "ca") # Test minuscule
        self.assertEqual(ticket["etat"], "CA")
        self.assertEqual(ticket["total_ht"], 60000.0)
        self.assertEqual(ticket["taux_reduction"], 0.15)
        self.assertEqual(ticket["total_ht_remise"], 51000.0)
        # TVA de 8.25% sur 51000 = 4207.5
        self.assertEqual(ticket["total_ttc"], 55207.5)

    def test_tous_les_taux_de_tva(self):
        """Vérifie la validité des taux de TVA pour chaque état avec un montant fixe de 100 HT."""
        etats_attendus = {
            'UT': 106.85,
            'NV': 108.00,
            'TX': 106.25,
            'AL': 104.00,
            'CA': 108.25
        }
        for etat, ttc_attendu in etats_attendus.items():
            ticket = CaisseEnregistreuse.generer_ticket("Article", 1, 100.0, etat)
            self.assertEqual(ticket["total_ttc"], ttc_attendu)

    def test_erreur_etat_inconnu(self):
        """Vérifie qu'une exception est levée si l'état n'existe pas."""
        with self.assertRaisesRegex(ValueError, "Le code d'état fourni est inconnu : 'FR'"):
            CaisseEnregistreuse.generer_ticket("Baguette", 1, 1.0, "FR")


if __name__ == '__main__':
    unittest.main()