import unittest
# On suppose que votre code sera dans un fichier nommé 'jukebox.py'
# et qu'il contiendra une fonction 'ajouter_chanson'
from jukebox import ajouter_chanson

class TestJukebox(unittest.TestCase):

    def test_ajouter_chanson_dans_file_vide(self):
        """Une chanson doit être ajoutée si la file est vide."""
        file_actuelle = []
        nouvelle_file = ajouter_chanson("Bohemian Rhapsody", file_actuelle)
        self.assertEqual(nouvelle_file, ["Bohemian Rhapsody"])

    def test_ajouter_chanson_differente(self):
        """Une chanson différente de la dernière doit être ajoutée à la fin."""
        file_actuelle = ["Bohemian Rhapsody", "Thriller"]
        nouvelle_file = ajouter_chanson("Hotel California", file_actuelle)
        self.assertEqual(nouvelle_file, ["Bohemian Rhapsody", "Thriller", "Hotel California"])

    def test_refuser_chanson_identique_au_bout_de_file(self):
        """Une chanson identique à la DERNIÈRE ajoutée ne doit pas être insérée."""
        file_actuelle = ["Bohemian Rhapsody", "Thriller"]
        nouvelle_file = ajouter_chanson("Thriller", file_actuelle)
        self.assertEqual(nouvelle_file, ["Bohemian Rhapsody", "Thriller"])

    def test_autoriser_chanson_deja_presente_mais_pas_en_dernier(self):
        """Une chanson peut être ajoutée si elle est déjà dans la file, tant qu'elle n'est pas en dernière position."""
        file_actuelle = ["Thriller", "Bohemian Rhapsody"]
        nouvelle_file = ajouter_chanson("Thriller", file_actuelle)
        self.assertEqual(nouvelle_file, ["Thriller", "Bohemian Rhapsody", "Thriller"])

if __name__ == '__main__':
    unittest.main()
