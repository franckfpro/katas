"""
Le Kata : Le Panier Anti-Gaspillage (The Smart Cart)
Énoncé
Dans le cadre d'une application de supermarché anti-gaspillage, les clients peuvent ajouter des articles en promotion à leur panier. Cependant, pour éviter les abus et le marché noir, le magasin impose une règle : un client ne peut pas acheter plus de 3 exemplaires du même article.

Si un utilisateur tente d'ajouter un article qui est déjà présent 3 fois dans son panier, le panier reste inchangé.

Spécifications de la fonction ajouter_au_panier
Elle prend en paramètre le nom de l'article (un str) et le panier actuel (une list[str]).

Elle renvoie le panier mis à jour (une list[str]).

Si l'article est présent moins de 3 fois (0, 1 ou 2 fois), il est ajouté à la fin de la liste.

Si l'article est déjà présent 3 fois, on ignore l'ajout.
"""

import unittest
# On suppose que votre code sera dans un fichier nommé 'panier.py'
#from panier import ajouter_au_panier

def ajouter_au_panier(
    article: str = "",
    panier: list[str] = [""]
) -> list[str]:
    count = 0
    for article_panier in panier:
        if article_panier == article:
            count += 1
    if count < 3:
        panier.append(article)
    return panier

class TestSmartCart(unittest.TestCase):

    def test_ajouter_article_panier_vide(self):
        """Un article doit être ajouté si le panier est vide."""
        panier_actuel = []
        nouveau_panier = ajouter_au_panier("Avocat", panier_actuel)
        self.assertEqual(nouveau_panier, ["Avocat"])

    def test_ajouter_article_sous_la_limite(self):
        """On peut ajouter un article s'il est présent moins de 3 fois."""
        panier_actuel = ["Avocat", "Banane", "Avocat"] # Déjà 2 avocats
        nouveau_panier = ajouter_au_panier("Avocat", panier_actuel)
        self.assertEqual(nouveau_panier, ["Avocat", "Banane", "Avocat", "Avocat"])

    def test_bloquer_article_si_limite_atteinte(self):
        """On ne doit pas pouvoir ajouter un article s'il est déjà présent 3 fois."""
        panier_actuel = ["Avocat", "Banane", "Avocat", "Avocat"] # Déjà 3 avocats
        nouveau_panier = ajouter_au_panier("Avocat", panier_actuel)
        # Le panier ne doit pas avoir bougé
        self.assertEqual(nouveau_panier, ["Avocat", "Banane", "Avocat", "Avocat"])

    def test_ajouter_autre_article_quand_un_est_bloque(self):
        """Le blocage d'un article n'empêche pas d'en ajouter un autre différent."""
        panier_actuel = ["Avocat", "Avocat", "Avocat"] # Avocats au max
        nouveau_panier = ajouter_au_panier("Banane", panier_actuel)
        self.assertEqual(nouveau_panier, ["Avocat", "Avocat", "Avocat", "Banane"])

if __name__ == '__main__':
    unittest.main(verbosity=0)

