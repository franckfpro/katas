"""
KATA PYTHON #047 - Le Compte Bancaire Sécurisé
Difficulté : 4/10

ÉNONCÉ :
Vous devez créer une classe `CompteBancaire` qui permet de gérer les opérations 
de base d'un client (dépôt, retrait, consultation) tout en appliquant des 
règles de gestion strictes.

On vous demande de compléter la classe `CompteBancaire` ci-dessous.

RÈGLES ET CONTRAINTES :
1. L'initialisation (`__init__`) prend un `titulaire` (str) et un `solde_initial` 
   (float ou int, par défaut à 0.0). Si le `solde_initial` fourni est négatif, 
   vous devez lever une exception de type `ValueError`.
2. La méthode `deposer(montant)` ajoute l'argent au solde. Si le montant est 
   inférieur ou égal à 0, l'opération doit lever une `ValueError`.
3. La méthode `retirer(montant)` soustrait l'argent du solde. 
   - Si le montant est inférieur ou égal à 0, lever une `ValueError`.
   - Si le solde est insuffisant pour couvrir le retrait, lever une exception 
     personnalisée `SoldeInsuffisantError` (déjà définie pour vous).
4. La méthode `obtenir_solde()` doit simplement renvoyer le solde actuel.
"""

import unittest


class SoldeInsuffisantError(Exception):
    """Exception levée lorsque le solde est insuffisant pour un retrait."""
    pass


class CompteBancaire:
    """Représente un compte bancaire avec gestion de solde et sécurité."""

    def __init__(self, titulaire: str, solde_initial: float = 0.0):
        """Initialise le compte avec un titulaire et un solde initial."""
        # TODO: Initialiser les attributs de l'objet et valider le solde_initial
        pass

    def deposer(self, montant: float) -> None:
        """Dépose de l'argent sur le compte."""
        # TODO: Implémenter la logique et les validations
        pass

    def retirer(self, montant: float) -> None:
        """Retire de l'argent du compte si le solde le permet."""
        # TODO: Implémenter la logique, les validations et l'exception sur mesure
        pass

    def obtenir_solde(self) -> float:
        """Renvoie le solde actuel du compte."""
        # TODO: Retourner le bon attribut
        pass


# =====================================================================
# TESTS UNITAIRES (Ne pas modifier cette section)
# =====================================================================

class TestCompteBancaire(unittest.TestCase):
    """Suite de tests pour valider la classe CompteBancaire."""

    def test_initialisation_valide(self):
        """Vérifie la création correcte d'un compte."""
        compte = CompteBancaire("Alice", 150.50)
        self.assertEqual(compte.titulaire, "Alice")
        self.assertEqual(compte.obtenir_solde(), 150.50)

    def test_initialisation_defaut(self):
        """Le solde doit être à 0.0 par défaut."""
        compte = CompteBancaire("Bob")
        self.assertEqual(compte.obtenir_solde(), 0.0)

    def test_initialisation_negative_invalide(self):
        """On ne peut pas créer un compte avec un solde négatif."""
        with self.assertRaises(ValueError):
            CompteBancaire("Charlie", -10.0)

    def test_depot_valide(self):
        """Un dépôt valide doit augmenter le solde."""
        compte = CompteBancaire("Alice", 100.0)
        compte.deposer(50.0)
        self.assertEqual(compte.obtenir_solde(), 150.0)

    def test_depot_invalide(self):
        """Un dépôt négatif ou nul doit lever une ValueError."""
        compte = CompteBancaire("Alice", 100.0)
        with self.assertRaises(ValueError):
            compte.deposer(-20.0)
        with self.assertRaises(ValueError):
            compte.deposer(0.0)

    def test_retrait_valide(self):
        """Un retrait valide doit diminuer le solde."""
        compte = CompteBancaire("Alice", 100.0)
        compte.retirer(40.0)
        self.assertEqual(compte.obtenir_solde(), 60.0)

    def test_retrait_invalide_montant(self):
        """Un retrait négatif ou nul doit lever une ValueError."""
        compte = CompteBancaire("Alice", 100.0)
        with self.assertRaises(ValueError):
            compte.retirer(-10.0)

    def test_retrait_solde_insuffisant(self):
        """Un retrait supérieur au solde doit lever SoldeInsuffisantError."""
        compte = CompteBancaire("Alice", 50.0)
        with self.assertRaises(SoldeInsuffisantError):
            compte.retirer(60.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)