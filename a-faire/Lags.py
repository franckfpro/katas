import unittest

# =====================================================================
# KATA : LAGS
# =====================================================================
#
# CONSIGNES :
# ABEAS Corp est une petite entreprise qui ne possède qu'un seul avion.
# Les clients d'ABEAS Corp demandent parfois à louer cet avion.
# Ils envoient une requête de location contenant :
# - Un identifiant de vol
# - Une heure de début (start time)
# - Une durée de voyage (travel duration)
# - Le prix qu'ils sont prêts à payer.
#
# Votre mission :
# Aider ABEAS Corp en trouvant la meilleure combinaison de requêtes 
# (qui ne se chevauchent pas) afin de maximiser le gain total.
#
# Exemple :
# La meilleure combinaison pour un certain fichier de 4 requêtes est 
# AF514 et BA01 pour un gain de 10 + 8 = 18.
# =====================================================================

class RequeteVol:
    def __init__(self, identifiant, debut, duree, prix):
        self.id = identifiant
        self.debut = debut
        self.duree = duree
        self.fin = debut + duree
        self.prix = prix

def maximiser_gain(requetes):
    """
    Calcule le gain maximum possible en choisissant des vols qui ne se chevauchent pas.
    Utilise la programmation dynamique pour une complexité temporelle de O(n log n).
    """
    if not requetes:
        return 0

    # 1. Trier les requêtes par heure de fin croissante
    requetes_triees = sorted(requetes, key=lambda r: r.fin)
    n = len(requetes_triees)
    
    # dp[i] stockera le gain maximum possible en utilisant un sous-ensemble des i premières requêtes
    dp = [0] * n
    dp[0] = requetes_triees[0].prix

    # 2. Remplir le tableau de programmation dynamique
    for i in range(1, n):
        gain_incluant_actuel = requetes_triees[i].prix
        
        # Trouver la dernière requête compatible (qui se termine avant ou pile quand la requête actuelle commence)
        # Pour un kata, une recherche linéaire inversée est suffisante. 
        # (Pour des performances optimales sur de très grands jeux de données, on utiliserait bisect/recherche binaire)
        dernier_compatible = -1
        for j in range(i - 1, -1, -1):
            if requetes_triees[j].fin <= requetes_triees[i].debut:
                dernier_compatible = j
                break
        
        # Si une requête compatible est trouvée, on ajoute son gain maximum au prix de la requête actuelle
        if dernier_compatible != -1:
            gain_incluant_actuel += dp[dernier_compatible]
            
        # Le gain maximum à l'étape i est le maximum entre :
        # - Le gain si on inclut la requête actuelle
        # - Le gain si on l'exclut (donc le gain maximum de l'étape précédente)
        gain_excluant_actuel = dp[i - 1]
        
        dp[i] = max(gain_incluant_actuel, gain_excluant_actuel)

    # Le dernier élément contient le gain maximum global
    return dp[-1]


# =====================================================================
# TESTS UNITAIRES
# =====================================================================

class TestLags(unittest.TestCase):

    def test_cas_nominal_enonce(self):
        """Doit retourner 18 avec la combinaison AF514 + BA01 comme décrit dans l'énoncé."""
        requetes = [
            RequeteVol("AF514", 0, 5, 10),
            RequeteVol("CO5", 3, 7, 14),
            RequeteVol("BA01", 5, 4, 8),
            RequeteVol("KLM02", 8, 2, 5)
        ]
        # AF514 (0->5, prix 10) et BA01 (5->9, prix 8) ne se chevauchent pas. Total = 18.
        self.assertEqual(maximiser_gain(requetes), 18)

    def test_aucun_vol(self):
        """Doit retourner 0 si la liste de requêtes est vide."""
        self.assertEqual(maximiser_gain([]), 0)

    def test_un_seul_vol(self):
        """Doit retourner le prix du seul vol disponible."""
        requetes = [RequeteVol("AF1", 2, 5, 100)]
        self.assertEqual(maximiser_gain(requetes), 100)

    def test_vols_totalement_incompatibles(self):
        """Doit retourner le vol le plus cher si aucun vol ne peut être combiné."""
        requetes = [
            RequeteVol("V1", 0, 10, 15),
            RequeteVol("V2", 2, 5, 50),
            RequeteVol("V3", 4, 3, 20)
        ]
        # Ils se chevauchent tous, on ne peut en prendre qu'un seul. Le meilleur est V2.
        self.assertEqual(maximiser_gain(requetes), 50)

    def test_vols_consecutifs(self):
        """Doit additionner tous les vols s'ils s'enchaînent parfaitement."""
        requetes = [
            RequeteVol("V1", 0, 2, 10),
            RequeteVol("V2", 2, 2, 10),
            RequeteVol("V3", 4, 2, 10)
        ]
        self.assertEqual(maximiser_gain(requetes), 30)

if __name__ == '__main__':
    unittest.main()