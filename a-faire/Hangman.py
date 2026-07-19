import unittest
from enum import Enum

"""
KATA HANGMAN (LE JEU DU PENDU)

Description du problème :
Le pendu est un célèbre jeu de devinettes de mots. Le joueur doit deviner un mot secret 
lettre par lettre. Les bonnes réponses révèlent la lettre dans le mot. Les mauvaises 
réponses s'accumulent. Si le nombre de mauvaises réponses dépasse la limite avant que 
le mot ne soit révélé, le joueur perd. S'il révèle tout le mot, il gagne !

Instructions :
1. Créez une classe `JeuDuPendu` pour représenter le jeu.
   - À l'initialisation, elle doit accepter un mot secret et le stocker en MAJUSCULES.
   - Elle doit stocker le nombre de mauvaises réponses entraînant la défaite.
   - Elle doit exposer une propriété indiquant que le jeu est "en cours".

2. Ajoutez une méthode `deviner(lettre)` qui renvoie un résultat :
   - Si la lettre n'est pas un caractère valide (ex: "A-Z"), renvoyer un résultat "Invalide".
   - Si la lettre n'est pas dans le mot, renvoyer "Incorrect" et l'ajouter à la liste des erreurs.
   - Si la lettre a déjà été essayée (bonne ou mauvaise), renvoyer "Duplicata".
   - Si la lettre est correcte et nouvelle, renvoyer "Valide".

3. Après chaque essai, calculez le nouvel état du jeu :
   - Si toutes les lettres ont été devinées, le jeu est "Gagné".
   - Si le nombre d'erreurs atteint la limite, le jeu est "Perdu".
   - Sinon, le jeu reste "En cours".
"""

# --- ÉNUMÉRATIONS POUR LES ÉTATS ET RÉSULTATS ---

class EtatJeu(Enum):
    EN_COURS = 1
    GAGNE = 2
    PERDU = 3

class ResultatEssai(Enum):
    VALIDE = 1
    INVALIDE = 2
    INCORRECT = 3
    DUPLICATA = 4


# --- IMPLÉMENTATION DE LA CLASSE ---

class JeuDuPendu:
    def __init__(self, mot_secret: str, max_erreurs: int):
        self.mot_secret = mot_secret.upper()
        self.max_erreurs = max_erreurs
        self.erreurs_actuelles = 0
        self.lettres_devinees = set()
        self.lettres_incorrectes = []
        self.etat = EtatJeu.EN_COURS

    def deviner(self, lettre: str) -> ResultatEssai:
        # Si le jeu est déjà terminé, on ne peut plus jouer
        if self.etat != EtatJeu.EN_COURS:
            return ResultatEssai.INVALIDE

        lettre = lettre.upper()

        # Règle 2.2 : Validation du caractère
        if not lettre.isalpha() or len(lettre) != 1:
            return ResultatEssai.INVALIDE

        # Règle 2.4 : Gestion des duplicatas
        if lettre in self.lettres_devinees or lettre in self.lettres_incorrectes:
            return ResultatEssai.DUPLICATA

        # Règle 2.3 et Vérification du succès
        if lettre in self.mot_secret:
            self.lettres_devinees.add(lettre)
            self._mettre_a_jour_etat()
            return ResultatEssai.VALIDE
        else:
            self.lettres_incorrectes.append(lettre)
            self.erreurs_actuelles += 1
            self._mettre_a_jour_etat()
            return ResultatEssai.INCORRECT

    def _mettre_a_jour_etat(self):
        """Méthode privée pour réévaluer l'état du jeu après chaque coup."""
        if self.erreurs_actuelles >= self.max_erreurs:
            self.etat = EtatJeu.PERDU
        # On vérifie si toutes les lettres uniques du mot secret ont été trouvées
        elif set(self.mot_secret).issubset(self.lettres_devinees):
            self.etat = EtatJeu.GAGNE


# --- TESTS UNITAIRES ---

class TestJeuDuPendu(unittest.TestCase):

    def setUp(self):
        # Initialise un jeu avant chaque test : mot secret "PYTHON", max 3 erreurs
        self.jeu = JeuDuPendu("Python", 3)

    def test_initialisation_jeu(self):
        """Vérifie le bon paramétrage au lancement du jeu."""
        self.assertEqual(self.jeu.mot_secret, "PYTHON")
        self.assertEqual(self.jeu.etat, EtatJeu.EN_COURS)
        self.assertEqual(self.jeu.max_erreurs, 3)

    def test_lettre_invalide(self):
        """Les chiffres ou caractères spéciaux doivent renvoyer INVALIDE."""
        self.assertEqual(self.jeu.deviner("1"), ResultatEssai.INVALIDE)
        self.assertEqual(self.jeu.deviner("@"), ResultatEssai.INVALIDE)
        self.assertEqual(self.jeu.deviner("AB"), ResultatEssai.INVALIDE) # Trop long

    def test_lettre_deja_devinee(self):
        """Rejouer une lettre doit renvoyer DUPLICATA."""
        self.jeu.deviner("P")
        self.assertEqual(self.jeu.deviner("P"), ResultatEssai.DUPLICATA)
        self.assertEqual(self.jeu.deviner("p"), ResultatEssai.DUPLICATA) # Casse ignorée

    def test_lettre_incorrecte(self):
        """Une lettre absente doit incrémenter les erreurs."""
        resultat = self.jeu.deviner("Z")
        self.assertEqual(resultat, ResultatEssai.INCORRECT)
        self.assertEqual(self.jeu.erreurs_actuelles, 1)
        self.assertIn("Z", self.jeu.lettres_incorrectes)

    def test_perdre_la_partie(self):
        """Le jeu doit passer à l'état PERDU si le max d'erreurs est atteint."""
        self.jeu.deviner("A") # 1 erreur
        self.jeu.deviner("B") # 2 erreurs
        self.jeu.deviner("C") # 3 erreurs
        self.assertEqual(self.jeu.etat, EtatJeu.PERDU)
        
        # Un coup après la défaite doit être invalide
        self.assertEqual(self.jeu.deviner("D"), ResultatEssai.INVALIDE)

    def test_gagner_la_partie(self):
        """Le jeu doit passer à l'état GAGNE si toutes les lettres sont trouvées."""
        for lettre in ["P", "Y", "T", "H", "O", "N"]:
            self.jeu.deviner(lettre)
            
        self.assertEqual(self.jeu.etat, EtatJeu.GAGNE)

if __name__ == '__main__':
    unittest.main()