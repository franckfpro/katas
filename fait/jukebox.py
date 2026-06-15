"""
Le Kata : Le Distributeur de Chansons (The Jukebox)
Énoncé
Vous devez créer une fonction ou une classe qui gère la file d'attente d'un jukebox. Pour l'instant, le jukebox a une règle très simple : il ne peut pas y avoir deux fois la même chanson d'affilée dans la file d'attente.

Si un utilisateur essaie d'ajouter une chanson qui est exactement la même que la dernière chanson ajoutée, le jukebox doit ignorer la demande (ou lever une exception, selon votre choix de design). Si la chanson est différente, elle est ajoutée à la fin de la liste.

Spécifications de la fonction ajouter_chanson
Elle prend en paramètre le titre de la chanson (une chaîne de caractères) et la file d'attente actuelle (une liste).

Elle renvoie la nouvelle file d'attente mise à jour.

Si la file est vide, la chanson est ajoutée sans problème.

Si la chanson est identique à la dernière chanson de la liste, la liste reste inchangée.
"""

def ajouter_chanson(chanson: str, file_d_attente: list[str]) -> list[str]:
    """
    Ajoute une chanson à la file d'attente si elle est différente 
    de la dernière chanson de la liste.
    """
    if not file_d_attente or file_d_attente[-1] != chanson:
        file_d_attente.append(chanson)
    return file_d_attente
