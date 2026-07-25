"""
======================================================================
KATA : VENDING MACHINE (Distributeur Automatique)
======================================================================

CONSIGNES :
L'objectif est de construire le "cerveau" d'un distributeur automatique. 
Il doit accepter de l'argent, rendre la monnaie, gérer les stocks et 
distribuer des produits. L'idée est de pratiquer le TDD de manière 
itérative.

Implémentez les fonctionnalités dans l'ordre ci-dessous :

1. Accepter les pièces
   Le distributeur accepte les pièces valides (nickels, dimes, quarters) 
   et rejette les invalides (pennies). Quand une pièce valide est insérée, 
   le montant est ajouté au solde actuel et l'affichage est mis à jour.
   S'il n'y a pas de pièce, l'écran affiche "INSERT COIN". Les pièces 
   rejetées vont dans le retour de monnaie (coin return).
   NOTE : Identifiez les pièces par leur poids et leur taille, pas par 
   un objet qui "connaît" sa valeur.

2. Sélectionner un produit
   Trois produits : cola (1.00$), chips (0.50$), candy (0.65$).
   Si on appuie sur le bouton et qu'il y a assez d'argent : le produit 
   est distribué et la machine affiche "THANK YOU". À la vérification 
   suivante de l'écran, il affiche "INSERT COIN" et le solde passe à 0.00$.
   S'il n'y a pas assez d'argent : la machine affiche "PRICE [prix]". 
   Aux vérifications suivantes, elle affiche "INSERT COIN" ou le solde 
   actuel.

3. Rendre la monnaie
   Lorsqu'un produit est sélectionné et qu'il coûte moins cher que 
   l'argent inséré, la différence est placée dans le retour de monnaie.

4. Rendre les pièces (Bouton d'annulation)
   Quand le bouton de retour est pressé, l'argent inséré par le client 
   est placé dans le retour de monnaie et l'écran affiche "INSERT COIN".

5. Rupture de stock (Sold Out)
   Si un article sélectionné n'est pas disponible, l'écran affiche 
   "SOLD OUT". À la vérification suivante, il affiche le solde actuel 
   ou "INSERT COIN" s'il n'y a pas d'argent.

6. Appoint exact seulement (Exact Change Only)
   Si la machine ne peut pas rendre la monnaie pour l'un des articles 
   qu'elle vend (à cause d'un manque de pièces dans sa caisse interne), 
   elle affiche "EXACT CHANGE ONLY" au lieu de "INSERT COIN".
======================================================================
"""

import unittest

# --- CONFIGURATION DES PIÈCES (Simulation de poids et taille) ---
# Format : (poids_en_grammes, taille_en_mm)
COIN_SPECS = {
    "NICKEL": (5.0, 21.21),  # Vaut 0.05$
    "DIME": (2.268, 17.91),  # Vaut 0.10$
    "QUARTER": (5.67, 24.26) # Vaut 0.25$
    # Le Penny (2.5g, 19.05mm) n'est pas dans ce dictionnaire et doit être rejeté.
}

# --- CODE MÉTIER À TESTER ET FAIRE ÉVOLUER ---
class VendingMachine:
    def __init__(self):
        self.current_amount = 0.0
        self.coin_return = []
        self._display_message = None

    def insert_coin(self, weight, size):
        """Identifie la pièce via ses caractéristiques physiques."""
        if (weight, size) == COIN_SPECS["NICKEL"]:
            self.current_amount += 0.05
        elif (weight, size) == COIN_SPECS["DIME"]:
            self.current_amount += 0.10
        elif (weight, size) == COIN_SPECS["QUARTER"]:
            self.current_amount += 0.25
        else:
            # Pièce non reconnue (ex: Penny), on la rejette
            self.coin_return.append((weight, size))

    def get_display(self):
        """Retourne ce qui doit être affiché sur l'écran LCD."""
        if self._display_message:
            msg = self._display_message
            self._display_message = None # L'écran se réinitialise après lecture
            return msg
        
        if self.current_amount == 0.0:
            return "INSERT COIN"
        else:
            return f"{self.current_amount:.2f}"

    def get_coin_return(self):
        """Renvoie le contenu du bac de retour de monnaie et le vide."""
        returned = self.coin_return.copy()
        self.coin_return.clear()
        return returned


# ======================================================================
# ZONE DE TESTS UNITAIRES
# ======================================================================
class TestVendingMachine(unittest.TestCase):
    
    def setUp(self):
        self.machine = VendingMachine()

    # --- FEATURE 1 : Accepter les pièces ---
    def test_display_insert_coin_when_empty(self):
        self.assertEqual(self.machine.get_display(), "INSERT COIN")

    def test_accept_nickel_updates_display(self):
        self.machine.insert_coin(5.0, 21.21) # Nickel
        self.assertEqual(self.machine.get_display(), "0.05")

    def test_accept_dime_updates_display(self):
        self.machine.insert_coin(2.268, 17.91) # Dime
        self.assertEqual(self.machine.get_display(), "0.10")

    def test_accept_quarter_updates_display(self):
        self.machine.insert_coin(5.67, 24.26) # Quarter
        self.assertEqual(self.machine.get_display(), "0.25")

    def test_accept_multiple_valid_coins(self):
        self.machine.insert_coin(5.67, 24.26) # Quarter
        self.machine.insert_coin(2.268, 17.91) # Dime
        self.assertEqual(self.machine.get_display(), "0.35")

    def test_reject_invalid_coin_like_penny(self):
        self.machine.insert_coin(2.5, 19.05) # Penny
        
        # L'écran ne doit pas changer
        self.assertEqual(self.machine.get_display(), "INSERT COIN")
        
        # La pièce doit être dans le retour de monnaie
        coin_return = self.machine.get_coin_return()
        self.assertEqual(len(coin_return), 1)
        self.assertEqual(coin_return[0], (2.5, 19.05))

    # --- FEATURE 2 : Sélectionner un produit (À FAIRE) ---
    # def test_vend_cola_when_exact_change_inserted(self):
    #     pass


if __name__ == '__main__':
    unittest.main()