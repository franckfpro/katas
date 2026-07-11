import unittest

"""
KATA BRAINFUCK

Description du problème :
Créez un interpréteur qui, à partir d'un programme Brainfuck valide, l'exécute 
et renvoie l'état de la mémoire à la fin de celui-ci.

Règles de base :
Le langage Brainfuck est constitué de :
- un programme (une chaîne de caractères) ;
- un tableau unidimensionnel d'au moins 30 000 cellules d'octets initialisées à zéro 
  (représentant des caractères ASCII) ;
- un pointeur de données mobile (initialisé sur l'octet le plus à gauche du tableau).

Les 8 commandes classiques :
> : Incrémente le pointeur de données.
< : Décrémente le pointeur de données.
+ : Incrémente l'octet pointé.
- : Décrémente l'octet pointé.
. : Affiche l'octet pointé (format ASCII).
, : Accepte un octet en entrée et stocke sa valeur dans l'octet pointé.
[ : Si l'octet pointé vaut zéro, saute à la commande située après le ] correspondant.
] : Si l'octet pointé est différent de zéro, retourne à la commande située après le [ correspondant.

Contraintes supplémentaires du Kata :
1. Si le pointeur est sur le premier octet et que la commande '<' est utilisée, 
   le pointeur est déplacé sur le dernier octet du tableau (boucle circulaire).
2. Les valeurs stockées dans le tableau ne peuvent pas être négatives. 
   Si vous décrémentez 0, vous revenez à 255. De même, 255 + 1 = 0.
3. Les instructions doivent être faciles à renommer (par ex. pour changer la syntaxe 
   en "OooWee" de Rick et Morty).
4. Il doit être facile d'ajouter de nouvelles instructions, par exemple :
   ! : place le pointeur directement à la fin du tableau de mémoire.
"""

class InterpreteurBrainfuck:
    def __init__(self, taille_memoire=30000):
        self.taille_memoire = taille_memoire
        self.memoire = [0] * self.taille_memoire
        self.pointeur = 0
        self.sortie = ""
        
        # Dictionnaire de syntaxe pour faciliter le renommage des instructions
        self.syntaxe = {
            'inc_ptr': '>',
            'dec_ptr': '<',
            'inc_val': '+',
            'dec_val': '-',
            'output': '.',
            'input': ',',
            'loop_start': '[',
            'loop_end': ']',
            'go_to_end': '!' # Nouvelle instruction personnalisée
        }

    def reinitialiser(self):
        """Remet la mémoire et le pointeur à zéro avant une nouvelle exécution."""
        self.memoire = [0] * self.taille_memoire
        self.pointeur = 0
        self.sortie = ""

    def configurer_syntaxe(self, nouvelle_syntaxe):
        """Permet de remplacer la syntaxe par défaut."""
        self.syntaxe.update(nouvelle_syntaxe)

    def _precalculer_sauts(self, code):
        """Parcourt le code pour associer les index des crochets ouvrants et fermants."""
        pile = []
        sauts = {}
        for i, char in enumerate(code):
            if char == self.syntaxe['loop_start']:
                pile.append(i)
            elif char == self.syntaxe['loop_end']:
                if not pile:
                    raise ValueError(f"Erreur de syntaxe : boucle fermante inattendue à l'index {i}")
                debut = pile.pop()
                sauts[debut] = i
                sauts[i] = debut
        if pile:
            raise ValueError("Erreur de syntaxe : boucle ouvrante non fermée")
        return sauts

    def executer(self, code, entrees=""):
        """Exécute le code Brainfuck et retourne l'état de la mémoire."""
        self.reinitialiser()
        sauts = self._precalculer_sauts(code)
        index_entree = 0
        pc = 0 # Program counter (index de l'instruction courante)

        while pc < len(code):
            char = code[pc]

            if char == self.syntaxe['inc_ptr']:
                self.pointeur = (self.pointeur + 1) % self.taille_memoire
            
            elif char == self.syntaxe['dec_ptr']:
                self.pointeur = (self.pointeur - 1) % self.taille_memoire
            
            elif char == self.syntaxe['inc_val']:
                self.memoire[self.pointeur] = (self.memoire[self.pointeur] + 1) % 256
            
            elif char == self.syntaxe['dec_val']:
                self.memoire[self.pointeur] = (self.memoire[self.pointeur] - 1) % 256
            
            elif char == self.syntaxe['output']:
                self.sortie += chr(self.memoire[self.pointeur])
            
            elif char == self.syntaxe['input']:
                if index_entree < len(entrees):
                    self.memoire[self.pointeur] = ord(entrees[index_entree])
                    index_entree += 1
                else:
                    self.memoire[self.pointeur] = 0 # Par défaut si plus d'entrée
            
            elif char == self.syntaxe['loop_start']:
                if self.memoire[self.pointeur] == 0:
                    pc = sauts[pc] # Saute à l'instruction après le crochet fermant
            
            elif char == self.syntaxe['loop_end']:
                if self.memoire[self.pointeur] != 0:
                    pc = sauts[pc] # Retourne au crochet ouvrant
            
            elif char == self.syntaxe['go_to_end']:
                self.pointeur = self.taille_memoire - 1
            
            pc += 1

        return self.memoire


# --- TESTS UNITAIRES ---

class TestInterpreteurBrainfuck(unittest.TestCase):
    def setUp(self):
        self.interpreteur = InterpreteurBrainfuck(taille_memoire=10) # Petite mémoire pour les tests

    def test_increment_decrement_valeur(self):
        memoire = self.interpreteur.executer("++-")
        self.assertEqual(memoire[0], 1)

    def test_boucle_circulaire_valeur(self):
        """Teste que 0 - 1 = 255 et 255 + 1 = 0"""
        memoire = self.interpreteur.executer("-")
        self.assertEqual(memoire[0], 255)
        
        memoire = self.interpreteur.executer("-+")
        self.assertEqual(memoire[0], 0)

    def test_deplacement_pointeur(self):
        memoire = self.interpreteur.executer(">+>++")
        self.assertEqual(memoire[0], 0)
        self.assertEqual(memoire[1], 1)
        self.assertEqual(memoire[2], 2)

    def test_boucle_circulaire_pointeur(self):
        """Teste que la commande '<' sur le premier octet renvoie à la fin."""
        memoire = self.interpreteur.executer("<+")
        # La taille de mémoire définie dans setUp est 10, donc le dernier index est 9
        self.assertEqual(memoire[9], 1)
        self.assertEqual(self.interpreteur.pointeur, 9)

    def test_boucle_simple(self):
        """Boucle qui décrémente la case 0 jusqu'à 0 et incrémente la case 1."""
        # Initialise à 3, puis transfert dans la case 1
        memoire = self.interpreteur.executer("+++[>+<-]")
        self.assertEqual(memoire[0], 0)
        self.assertEqual(memoire[1], 3)

    def test_entree_sortie(self):
        """Teste la lecture d'une chaîne et son affichage."""
        self.interpreteur.executer(",.,.", entrees="Hi")
        self.assertEqual(self.interpreteur.sortie, "Hi")

    def test_instruction_personnalisee_fin_memoire(self):
        """Teste l'instruction '!' qui place le pointeur à la fin du tableau."""
        memoire = self.interpreteur.executer("!+")
        self.assertEqual(memoire[9], 1)
        self.assertEqual(self.interpreteur.pointeur, 9)

    def test_changement_syntaxe(self):
        """Teste la robustesse en modifiant la syntaxe de base."""
        nouvelle_syntaxe = {
            'inc_val': 'Ooo',
            'dec_val': 'Wee',
            'inc_ptr': 'Rick',
            'dec_ptr': 'Morty'
        }
        self.interpreteur.configurer_syntaxe(nouvelle_syntaxe)
        # Ooo (0->1), Ooo (1->2), Rick (ptr+1), Ooo (0->1)
        memoire = self.interpreteur.executer("OooOooRickOoo")
        self.assertEqual(memoire[0], 2)
        self.assertEqual(memoire[1], 1)

if __name__ == '__main__':
    unittest.main()