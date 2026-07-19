import random
import unittest
from unittest.mock import patch

"""
KATA QUOTE OF THE DAY (Citation du jour)
========================================

Description :
Vous devez écrire un service web (ici simulé par une fonction) qui retourne 
une citation différente (aléatoire) à chaque fois que vous l'appelez. 

Exigence supplémentaire : 
Si vous ajoutez un paramètre de recherche (équivalent à `?q=foobar` dans une URL), 
le service doit retourner une citation aléatoire qui contient la chaîne de 
caractères "foobar" (insensible à la casse).

Indices :
L'objectif est d'avancer à petits pas (Baby Steps). 
L'utilisation d'un langage de script comme Python rend la manipulation des 
chaînes et de l'aléatoire très simple.
"""

# Base de données simulée de citations pour notre service
QUOTES = [
    "La simplicité est la sophistication suprême.",
    "Le code est lu beaucoup plus souvent qu'il n'est écrit.",
    "Un problème sans solution est un problème mal posé.",
    "L'art de la programmation est l'art d'organiser la complexité.",
    "Faites simple, faites-le bien."
]

def get_quote_of_the_day(query: str = None) -> str:
    """
    Retourne une citation aléatoire. 
    Si un paramètre 'query' est fourni, filtre les citations contenant 
    cette sous-chaîne (insensible à la casse) avant d'en choisir une au hasard.
    """
    if query:
        # Filtrage insensible à la casse
        filtered_quotes = [q for q in QUOTES if query.lower() in q.lower()]
        
        # Gestion du cas où aucune citation ne correspond
        if not filtered_quotes:
            return "Aucune citation trouvée pour cette recherche."
            
        return random.choice(filtered_quotes)
    
    # Comportement par défaut : citation aléatoire sur toute la liste
    return random.choice(QUOTES)


class TestQuoteOfTheDay(unittest.TestCase):
    
    def test_returns_a_quote_from_the_list(self):
        # Vérifie que la fonction retourne bien une citation issue de notre base
        quote = get_quote_of_the_day()
        self.assertIn(quote, QUOTES)
        
    @patch('random.choice')
    def test_returns_random_quote(self, mock_choice):
        # Vérifie que la fonction utilise bien l'aléatoire pour choisir (Mock)
        mock_choice.return_value = QUOTES[1]
        
        quote = get_quote_of_the_day()
        
        self.assertEqual(quote, QUOTES[1])
        mock_choice.assert_called_once()
        
    def test_returns_quote_matching_query(self):
        # Cherche le mot "code", qui n'est présent que dans une seule citation
        quote = get_quote_of_the_day("code")
        self.assertEqual(quote, "Le code est lu beaucoup plus souvent qu'il n'est écrit.")
        
    def test_returns_quote_matching_query_case_insensitive(self):
        # Cherche "SIMPLICITÉ" en majuscules pour vérifier l'insensibilité à la casse
        quote = get_quote_of_the_day("SIMPLICITÉ")
        self.assertEqual(quote, "La simplicité est la sophistication suprême.")
        
    @patch('random.choice')
    def test_returns_random_quote_among_multiple_matches(self, mock_choice):
        # Cherche le mot "art", qui est présent deux fois dans la même citation
        # On s'assure que random.choice est bien appelé sur la liste filtrée
        mock_choice.return_value = QUOTES[3]
        
        quote = get_quote_of_the_day("art")
        
        self.assertEqual(quote, "L'art de la programmation est l'art d'organiser la complexité.")
        mock_choice.assert_called_once_with([QUOTES[3]])
        
    def test_returns_not_found_message_if_no_match(self):
        # Cherche un mot inexistant dans la base
        quote = get_quote_of_the_day("éléphant")
        self.assertEqual(quote, "Aucune citation trouvée pour cette recherche.")

if __name__ == '__main__':
    unittest.main()