import unittest

"""
KATA DIGISIM (Simulateur de circuits logiques)

Description du problème :
L'objectif de ce kata est de développer un logiciel de simulation de montages
électroniques combinatoires à l'aide de portes réalisant les opérateurs logiques
de base. 

Un circuit sera vu comme un assemblage d'éléments actifs (les portes
logiques) et d'éléments passifs (les connexions). Une borne peut être utilisée
comme l'entrée d'un élément actif (qui fixe la valeur à un moment donné) ou
comme la sortie d'un élément actif (ce qui permet de recueillir la valeur
calculée). 

Un dispositif comportera donc une ou plusieurs entrées et une ou plusieurs sorties. 
Par exemple :
- Porte AND à deux entrées (2 entrées, une sortie)
- Demi-additionneur (2 entrées et 2 sorties : la somme et la retenue) 

On doit pouvoir connecter les composants entre eux pour réaliser un circuit
logique. Quand l'assemblage a été créé, un appel à la méthode `value()`
déclenche le calcul de la valeur de sortie (à partir des valeurs d'entrée –
directes et/ou indirectes). Les valeurs sont booléennes. 

Il faut implémenter les composants suivants :
  - Unaires : NOT
  - Binaires : AND, NAND, NOR, OR, XNOR, XOR
  - N-aires : ANDn, ORn
  
Et les composants d'addition suivants (construits à l'aide des composants précédents) :
  - Half adder (Demi-additionneur)
  - Full adder (Additionneur complet)
  - Adder sur n bits (Additionneur N bits)
"""

# --- INFRASTRUCTURE ET CONNECTIQUE ---

class Noeud:
    """Classe de base représentant tout composant ayant une valeur de sortie."""
    def value(self) -> bool:
        raise NotImplementedError

class Entree(Noeud):
    """Représente une entrée basique du circuit (0 ou 1) que l'on peut modifier."""
    def __init__(self, etat: bool = False):
        self.etat = etat

    def definir(self, etat: bool):
        self.etat = etat

    def value(self) -> bool:
        return self.etat

class PorteLogique(Noeud):
    """Classe parente pour les portes logiques. Gère les connexions en entrée."""
    def __init__(self, *entrees):
        # Si une entrée est un booléen simple, on la convertit en noeud `Entree`
        self.entrees = [e if isinstance(e, Noeud) else Entree(e) for e in entrees]

    def valeurs_entrees(self) -> list[bool]:
        """Évalue de manière récursive toutes les entrées connectées."""
        return [e.value() for e in self.entrees]


# --- PORTES LOGIQUES DE BASE ---

class Not(PorteLogique):
    def value(self) -> bool:
        return not self.valeurs_entrees()[0]

class And(PorteLogique):
    def value(self) -> bool:
        v = self.valeurs_entrees()
        return v[0] and v[1]

class Nand(PorteLogique):
    def value(self) -> bool:
        v = self.valeurs_entrees()
        return not (v[0] and v[1])

class Or(PorteLogique):
    def value(self) -> bool:
        v = self.valeurs_entrees()
        return v[0] or v[1]

class Nor(PorteLogique):
    def value(self) -> bool:
        v = self.valeurs_entrees()
        return not (v[0] or v[1])

class Xor(PorteLogique):
    def value(self) -> bool:
        v = self.valeurs_entrees()
        return v[0] ^ v[1]

class Xnor(PorteLogique):
    def value(self) -> bool:
        v = self.valeurs_entrees()
        return not (v[0] ^ v[1])

class AndN(PorteLogique):
    def value(self) -> bool:
        return all(self.valeurs_entrees())

class OrN(PorteLogique):
    def value(self) -> bool:
        return any(self.valeurs_entrees())


# --- COMPOSANTS COMPLEXES (ADDITIONNEURS) ---

class HalfAdder:
    """Demi-additionneur. Possède 2 sorties : Somme et Retenue (Carry)."""
    def __init__(self, a: Noeud, b: Noeud):
        self.somme = Xor(a, b)
        self.retenue = And(a, b)

    def value(self) -> tuple[bool, bool]:
        """Retourne (Somme, Retenue)"""
        return (self.somme.value(), self.retenue.value())

class FullAdder:
    """Additionneur complet. Construit en combinant des demi-additionneurs."""
    def __init__(self, a: Noeud, b: Noeud, cin: Noeud):
        self.ha1 = HalfAdder(a, b)
        # On peut brancher la sortie 'somme' du HA1 (qui est un noeud Xor) sur le HA2
        self.ha2 = HalfAdder(self.ha1.somme, cin)
        
        self.somme = self.ha2.somme
        self.retenue = Or(self.ha1.retenue, self.ha2.retenue)

    def value(self) -> tuple[bool, bool]:
        """Retourne (Somme, Retenue)"""
        return (self.somme.value(), self.retenue.value())

class NBitAdder:
    """Additionneur sur N bits. Entrées: listes de bits du poids faible (LSB) au fort (MSB)."""
    def __init__(self, a_bits: list[Noeud], b_bits: list[Noeud], cin: Noeud):
        assert len(a_bits) == len(b_bits), "Les opérandes doivent avoir la même taille"
        
        self.sorties_somme = []
        c_courant = cin
        
        for a, b in zip(a_bits, b_bits):
            fa = FullAdder(a, b, c_courant)
            self.sorties_somme.append(fa.somme)
            c_courant = fa.retenue # La retenue sortante devient l'entrée du suivant
            
        self.retenue_finale = c_courant

    def value(self) -> tuple[list[bool], bool]:
        """Retourne ([Liste des sommes], Retenue finale)"""
        return ([s.value() for s in self.sorties_somme], self.retenue_finale.value())


# --- TESTS UNITAIRES ---

class TestDigiSim(unittest.TestCase):

    def test_porte_not(self):
        self.assertFalse(Not(True).value())
        self.assertTrue(Not(False).value())

    def test_porte_and(self):
        self.assertFalse(And(False, False).value())
        self.assertFalse(And(False, True).value())
        self.assertFalse(And(True, False).value())
        self.assertTrue(And(True, True).value())

    def test_porte_or(self):
        self.assertFalse(Or(False, False).value())
        self.assertTrue(Or(False, True).value())
        self.assertTrue(Or(True, False).value())
        self.assertTrue(Or(True, True).value())

    def test_porte_xor(self):
        self.assertFalse(Xor(False, False).value())
        self.assertTrue(Xor(False, True).value())
        self.assertTrue(Xor(True, False).value())
        self.assertFalse(Xor(True, True).value())

    def test_portes_n_aires(self):
        # ANDn
        self.assertTrue(AndN(True, True, True).value())
        self.assertFalse(AndN(True, False, True).value())
        # ORn
        self.assertFalse(OrN(False, False, False).value())
        self.assertTrue(OrN(False, True, False).value())

    def test_evaluation_dynamique_circuit(self):
        """Teste qu'un changement sur une entrée propage le résultat lors de l'appel à value()"""
        entree_a = Entree(False)
        entree_b = Entree(True)
        circuit = And(entree_a, Or(entree_a, entree_b))
        
        self.assertFalse(circuit.value()) # False AND (False OR True) -> False
        
        # Modification dynamique des valeurs
        entree_a.definir(True)
        self.assertTrue(circuit.value()) # True AND (True OR True) -> True

    def test_half_adder(self):
        """Vérifie la table de vérité du demi-additionneur (Somme, Retenue)"""
        # A=0, B=0 -> Somme=0, Retenue=0
        self.assertEqual(HalfAdder(False, False).value(), (False, False))
        # A=1, B=0 -> Somme=1, Retenue=0
        self.assertEqual(HalfAdder(True, False).value(), (True, False))
        # A=1, B=1 -> Somme=0, Retenue=1
        self.assertEqual(HalfAdder(True, True).value(), (False, True))

    def test_full_adder(self):
        """Vérifie la table de vérité de l'additionneur complet (Somme, Retenue)"""
        # A=0, B=0, Cin=0
        self.assertEqual(FullAdder(False, False, False).value(), (False, False))
        # A=1, B=0, Cin=0
        self.assertEqual(FullAdder(True, False, False).value(), (True, False))
        # A=1, B=1, Cin=0 -> 1+1=2 (Somme=0, Retenue=1)
        self.assertEqual(FullAdder(True, True, False).value(), (False, True))
        # A=1, B=1, Cin=1 -> 1+1+1=3 (Somme=1, Retenue=1)
        self.assertEqual(FullAdder(True, True, True).value(), (True, True))

    def test_n_bit_adder(self):
        """Addition de deux nombres sur 3 bits. Les bits sont ordonnés LSB -> MSB."""
        # Nombre A : 3 (en binaire LSB: 1, 1, 0)
        A = [Entree(True), Entree(True), Entree(False)]
        # Nombre B : 2 (en binaire LSB: 0, 1, 0)
        B = [Entree(False), Entree(True), Entree(False)]
        Cin = Entree(False)

        adder = NBitAdder(A, B, Cin)
        sommes, retenue = adder.value()

        # Attendu: 3 + 2 = 5 (en binaire LSB: 1, 0, 1) avec Retenue = 0
        self.assertEqual(sommes, [True, False, True])
        self.assertFalse(retenue)

if __name__ == '__main__':
    unittest.main()