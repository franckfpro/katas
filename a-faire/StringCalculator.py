import unittest
import re

"""
KATA STRING CALCULATOR (Calculatrice de chaînes de caractères)

Consignes combinées :
Ce kata est conçu pour vous aider à apprendre la programmation dirigée par les tests (TDD) et la refactorisation. Travaillez de manière incrémentale.

Étapes à implémenter :
1. Créez une fonction `add(nombres)` qui prend une chaîne de caractères et renvoie un entier.
   - Une chaîne vide doit renvoyer 0.
   - La méthode peut prendre 0, 1 ou 2 nombres séparés par des virgules (ex: "1,2") et renvoie leur somme.
2. Autorisez la méthode à gérer un nombre inconnu d'arguments.
3. Autorisez la méthode à gérer les retours à la ligne ('\\n') comme séparateurs, en plus des virgules (ex: "1\\n2,3" renvoie 6).
4. Autorisez un délimiteur personnalisé.
   - Pour changer le délimiteur, le début de la chaîne doit contenir une ligne formatée ainsi : "//[délimiteur]\\n[nombres]".
   - Exemple : "//;\\n1;2" renvoie 3.
5. Appeler `add` avec un ou plusieurs nombres négatifs doit lever une exception indiquant "Nombres négatifs non autorisés :" suivi de tous les nombres négatifs trouvés.
6. Les nombres strictement supérieurs à 1000 doivent être ignorés (ex: "1001,2" renvoie 2).
7. Les délimiteurs personnalisés peuvent avoir n'importe quelle longueur en utilisant la syntaxe : "//[délimiteur_long]\\n[nombres]" (ex: "//[***]\\n1***2***3" renvoie 6).
8. Autorisez plusieurs délimiteurs avec la syntaxe : "//[delim1][delim2]\\n[nombres]" (ex: "//[*][%]\\n1*2%3" renvoie 6).
9. Gérez plusieurs délimiteurs de n'importe quelle longueur.
"""

def add(nombres: str) -> int:
    """
    Calcule la somme des nombres contenus dans une chaîne de caractères 
    en respectant les règles du String Calculator.
    """
    if not nombres:
        return 0

    delimiteurs = [",", "\n"]
    chaine_a_traiter = nombres

    # Étape 4, 7, 8, 9 : Gestion des délimiteurs personnalisés
    if nombres.startswith("//"):
        parties = nombres.split("\n", 1)
        ligne_delimiteur = parties[0][2:] # On retire le "//" initial
        chaine_a_traiter = parties[1]

        # Vérifie si la syntaxe utilise des crochets pour les délimiteurs longs ou multiples
        if ligne_delimiteur.startswith("[") and ligne_delimiteur.endswith("]"):
            delimiteurs_custom = re.findall(r'\[(.*?)\]', ligne_delimiteur)
            delimiteurs.extend(delimiteurs_custom)
        else:
            # Délimiteur simple d'un seul caractère
            delimiteurs.append(ligne_delimiteur)

    # Échapper les délimiteurs pour éviter les conflits avec les caractères spéciaux Regex (ex: '*')
    pattern = '|'.join(map(re.escape, delimiteurs))
    tokens = re.split(pattern, chaine_a_traiter)

    somme = 0
    negatifs = []

    # Étape 1, 2, 5, 6 : Conversion, filtrage et somme
    for token in tokens:
        if not token.strip():
            continue
        
        valeur = int(token)
        
        if valeur < 0:
            negatifs.append(valeur)
        elif valeur <= 1000:
            somme += valeur

    if negatifs:
        # Étape 5 : Lève une exception si des négatifs sont présents
        nombres_en_erreur = ", ".join(map(str, negatifs))
        raise ValueError(f"Nombres négatifs non autorisés : {nombres_en_erreur}")

    return somme


# --- TESTS UNITAIRES ---

class TestStringCalculator(unittest.TestCase):

    def test_chaine_vide_renvoie_zero(self):
        """Étape 1 : Chaîne vide."""
        self.assertEqual(add(""), 0)

    def test_un_nombre_renvoie_valeur(self):
        """Étape 1 : Un seul nombre."""
        self.assertEqual(add("1"), 1)

    def test_deux_nombres_renvoient_somme(self):
        """Étape 1 : Deux nombres séparés par une virgule."""
        self.assertEqual(add("1,2"), 3)

    def test_nombre_inconnu_d_arguments(self):
        """Étape 2 : Un nombre arbitraire d'arguments."""
        self.assertEqual(add("1,2,3,4,5"), 15)

    def test_separateur_retour_a_la_ligne(self):
        """Étape 3 : Gérer le caractère de nouvelle ligne comme séparateur."""
        self.assertEqual(add("1\n2,3"), 6)

    def test_delimiteur_personnalise_simple(self):
        """Étape 4 : Délimiteur personnalisé sur une ligne séparée."""
        self.assertEqual(add("//;\n1;2"), 3)

    def test_nombres_negatifs_levent_exception(self):
        """Étape 5 : Lancer une exception en cas de nombres négatifs."""
        with self.assertRaises(ValueError) as contexte:
            add("-1,2,-3")
        self.assertEqual(str(contexte.exception), "Nombres négatifs non autorisés : -1, -3")

    def test_ignorer_nombres_superieurs_a_1000(self):
        """Étape 6 : Ignorer les nombres de plus de 1000."""
        self.assertEqual(add("2,1001"), 2)
        self.assertEqual(add("1000,2"), 1002) # 1000 est inclus, 1001 est ignoré

    def test_delimiteur_longueur_variable(self):
        """Étape 7 : Gérer les délimiteurs de plusieurs caractères."""
        self.assertEqual(add("//[***]\n1***2***3"), 6)

    def test_plusieurs_delimiteurs(self):
        """Étape 8 : Gérer de multiples délimiteurs personnalisés."""
        self.assertEqual(add("//[*][%]\n1*2%3"), 6)

    def test_plusieurs_delimiteurs_de_longueur_variable(self):
        """Étape 9 : Combinaison de plusieurs délimiteurs longs."""
        self.assertEqual(add("//[***][#][%]\n1***2#3%4"), 10)


if __name__ == '__main__':
    unittest.main()