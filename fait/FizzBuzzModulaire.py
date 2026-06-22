"""
KATA PYTHON #042 - Le FizzBuzz Modulaire
Difficulté : 3/10

ÉNONCÉ :
On vous demande de créer une fonction `fizz_buzz_custom` qui prend en paramètre
un nombre entier positif `n` et un dictionnaire `regles`. 
Le dictionnaire contient des nombres entiers en clés et des chaînes de 
caractères en valeurs (ex: {3: "Fizz", 5: "Buzz"}).

La fonction doit retourner une liste des représentations sous forme de chaîne
de caractères de 1 à `n` inclus. Cependant :
- Si le nombre est divisible par une ou plusieurs clés du dictionnaire, on 
  remplace le nombre par la concaténation des valeurs correspondantes (dans 
  l'ordre croissant des clés).
- Sinon, on garde le nombre sous forme de chaîne de caractères (ex: "1").

Exemple avec regles = {3: "Fizz", 5: "Buzz"} et n = 5 :
Résultat attendu : ["1", "2", "Fizz", "4", "Buzz"]
"""

import unittest


def fizz_buzz_custom(n: int, regles: dict[int, str]) -> list[str]:
    """Génère la suite FizzBuzz personnalisée de 1 à n selon les règles fournies.

    Les règles doivent être appliquées dans l'ordre croissant des clés.
    """
    resultat = []
    for nbr in range(1,n+1):
        resultat.append(str(nbr))
        for k,v in regles.items():
            if nbr % k == 0:
                if resultat[nbr-1] == str(nbr):
                    resultat[nbr-1] = ""
                entry = resultat[nbr-1] + v
                resultat[nbr-1]=entry
    return resultat

"""
+ efficace:
resultat = []
    cles_triees = sorted(regles.keys())

    for i in range(1, n + 1):
        fragments = []
        for cle in cles_triees:
            if i % cle == 0:
                fragments.append(regles[cle])

        if fragments:
            resultat.append("".join(fragments))
        else:
            resultat.append(str(i))

    return resultat

"""


# =====================================================================
# TESTS UNITAIRES
# =====================================================================

class TestFizzBuzzCustom(unittest.TestCase):
    """Suite de tests pour valider le comportement de fizz_buzz_custom."""

    def setUp(self):
        """Initialisation des jeux de données de test."""
        self.regles_classiques = {3: "Fizz", 5: "Buzz"}
        self.regles_complexes = {2: "Foo", 4: "Bar", 7: "Baz"}

    def test_cas_classique_fizzbuzz(self):
        """Vérifie le comportement standard de FizzBuzz jusqu'à 15."""
        attendu = [
            "1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz",
            "11", "Fizz", "13", "14", "FizzBuzz"
        ]
        self.assertEqual(fizz_buzz_custom(15, self.regles_classiques), attendu)

    def test_dictionnaire_vide(self):
        """Si aucune règle, on ne doit obtenir que des nombres en string."""
        attendu = ["1", "2", "3", "4", "5"]
        self.assertEqual(fizz_buzz_custom(5, {}), attendu)

    def test_cles_non_ordonnees(self):
        """Vérifie que l'ordre des clés dans le dictionnaire n'importe pas."""
        regles_desordonnees = {5: "Buzz", 3: "Fizz"}
        attendu = ["1", "2", "Fizz", "4", "Buzz", "Fizz"]
        self.assertEqual(fizz_buzz_custom(6, regles_desordonnees), attendu)

    def test_regles_multiples(self):
        """Test avec 3 règles imbriquées pour vérifier les concaténations."""
        # 4 est divisible par 2 et 4 -> FooBar
        # 14 est divisible par 2 et 7 -> FooBaz
        attendu = [
            "1", "Foo", "3", "FooBar", "5", "Foo", "Baz", 
            "FooBar", "9", "Foo", "11", "FooBar", "13", "FooBaz"
        ]
        self.assertEqual(fizz_buzz_custom(14, self.regles_complexes), attendu)


if __name__ == "__main__":
    # Lancement des tests avec un feedback détaillé dans la console
    unittest.main(verbosity=0)
