import unittest

"""
KATA REMPLACEMENT DE DICTIONNAIRE (Dictionary Replacer)

Description du problème :
Ce kata consiste à créer un outil simple de remplacement de texte. 
Il s'inspire d'une présentation (Lightning talk) de Corey Haines sur la 
pratique du code.

Règles :
Créez une fonction qui prend en paramètres une chaîne de caractères et un dictionnaire.
La fonction doit remplacer chaque clé du dictionnaire trouvée dans la chaîne 
(préfixée et suffixée par un signe dollar '$') par la valeur correspondante 
définie dans le dictionnaire.

Exemples attendus :
1. Entrée : "", dictionnaire vide -> Sortie : ""
2. Entrée : "$temp$", dictionnaire : {"temp": "temporary"} -> Sortie : "temporary"
3. Entrée : "$temp$ here comes the name $name$", 
   dictionnaire : {"temp": "temporary", "name": "John Doe"} 
   -> Sortie : "temporary here comes the name John Doe"
"""

def remplacer_dictionnaire(texte: str, dictionnaire: dict[str, str]) -> str:
    """
    Remplace les clés du dictionnaire formatées en '$cle$' dans le texte 
    par leurs valeurs correspondantes.
    """
    # Si la chaîne est vide ou le dictionnaire est vide, on retourne le texte tel quel
    if not texte or not dictionnaire:
        return texte
        
    resultat = texte
    
    # On itère sur chaque paire clé/valeur du dictionnaire
    for cle, valeur in dictionnaire.items():
        # On formate la clé avec les balises '$' et on remplace dans le texte
        balise = f"${cle}$"
        resultat = resultat.replace(balise, valeur)
        
    return resultat


# --- TESTS UNITAIRES ---

class TestRemplacementDictionnaire(unittest.TestCase):
    
    def test_chaine_vide_et_dictionnaire_vide(self):
        """Test avec une chaîne et un dictionnaire vides."""
        self.assertEqual(remplacer_dictionnaire("", {}), "")

    def test_remplacement_unique(self):
        """Test avec une seule clé à remplacer formant toute la chaîne."""
        dictionnaire = {"temp": "temporary"}
        texte = "$temp$"
        attendu = "temporary"
        self.assertEqual(remplacer_dictionnaire(texte, dictionnaire), attendu)

    def test_remplacements_multiples_avec_texte(self):
        """Test avec plusieurs clés entremêlées dans du texte statique."""
        dictionnaire = {
            "temp": "temporary", 
            "name": "John Doe"
        }
        texte = "$temp$ here comes the name $name$"
        attendu = "temporary here comes the name John Doe"
        self.assertEqual(remplacer_dictionnaire(texte, dictionnaire), attendu)

    def test_balise_inexistante_dans_dictionnaire(self):
        """Vérifie qu'une balise n'étant pas dans le dictionnaire n'est pas altérée."""
        dictionnaire = {"temp": "temporary"}
        texte = "$temp$ et $inconnu$"
        attendu = "temporary et $inconnu$"
        self.assertEqual(remplacer_dictionnaire(texte, dictionnaire), attendu)


if __name__ == '__main__':
    unittest.main()