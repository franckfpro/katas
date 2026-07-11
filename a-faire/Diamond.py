import unittest

"""
KATA DIAMOND (DIAMANT)

Description du problème :
Étant donné une lettre de l'alphabet, écrivez une fonction qui affiche un diamant 
commençant par 'A', avec la lettre fournie située au point le plus large.

Par exemple, si la lettre fournie est 'C', le résultat imprimé doit être :
  A  
 B B 
C   C
 B B 
  A  

Règles :
1. Le diamant comporte toujours la lettre 'A' sur la première et la dernière ligne.
2. Chaque ligne (à l'exception de la ligne 'A') contient exactement deux occurrences 
   de la même lettre, séparées par des espaces.
3. La lettre fournie détermine la largeur maximale et la hauteur totale du diamant.
4. La forme est parfaitement symétrique horizontalement et verticalement (les 
   espaces extérieurs doivent donc être équilibrés).
"""

def generer_diamant(lettre: str) -> str:
    """
    Génère un diamant sous forme de chaîne de caractères à partir d'une lettre cible.
    """
    lettre = lettre.upper()
    if not 'A' <= lettre <= 'Z':
        raise ValueError("L'entrée doit être une lettre de l'alphabet (A-Z).")
        
    # Calcul de la distance entre 'A' et la lettre cible (A=0, B=1, C=2...)
    n = ord(lettre) - ord('A')
    lignes = []
    
    # Construction de la moitié supérieure (incluant la ligne centrale)
    for i in range(n + 1):
        char = chr(ord('A') + i)
        espaces_ext = " " * (n - i)
        
        if i ==