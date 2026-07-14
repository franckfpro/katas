import unittest

"""
KATA : ANNÉES BISSEXTILES (LEAP YEARS)

À propos de ce Kata :
Ce kata court et simple est idéal pour être réalisé en binôme en utilisant 
le Développement Dirigé par les Tests (TDD).

Contexte historique :
Avant 1582, le calendrier julien était largement utilisé et définissait comme 
bissextile toute année divisible par 4. Cependant, on a découvert à la fin du 
XVIe siècle que l'année civile s'était décalée par rapport à l'année solaire 
d'environ 10 jours. Le calendrier grégorien a été défini afin de réduire le 
nombre d'années bissextiles et d'aligner plus fidèlement l'année civile sur 
l'année solaire.

User Story :
En tant qu'utilisateur, je veux savoir si une année est bissextile, afin de 
pouvoir prévoir un jour supplémentaire le 29 février lors de ces années.

Critères d'acceptation (Les Règles) :
1. Toutes les années divisibles par 400 SONT bissextiles 
   (ex: 2000 était bien bissextile).
2. Toutes les années divisibles par 100 mais pas par 400 NE SONT PAS bissextiles 
   (ex: 1700, 1800 et 1900 ne l'étaient pas, 2100 ne le sera pas non plus).
3. Toutes les années divisibles par 4 mais pas par 100 SONT bissextiles 
   (ex: 2008, 2012, 2016).
4. Toutes les années non divisibles par 4 NE SONT PAS bissextiles 
   (ex: 2017, 2018, 2019).

Extension (Optionnelle pour aller plus loin) :
Le calendrier grégorien pourrait être rendu encore plus précis en ajoutant 
une règle qui élimine les années divisibles par 4000.
"""

def is_leap_year(year: int) -> bool:
    """
    Évalue si une année donnée est bissextile en suivant les critères 
    du calendrier grégorien.
    """
    # Règle 1 : Divisible par 400 -> Bissextile
    if year % 400 == 0:
        return True
        
    # Règle 2 : Divisible par 100 (mais pas 400) -> Pas bissextile
    if year % 100 == 0:
        return False
        
    # Règle 3 : Divisible par 4 (mais pas 100) -> Bissextile
    if year % 4 == 0:
        return True
        
    # Règle 4 : Non divisible par 4 -> Pas bissextile
    return False

    # Note : L'algorithme complet peut aussi s'écrire en une seule ligne :
    # return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)


# --- TESTS UNITAIRES ---

class TestLeapYears(unittest.TestCase):

    def test_divisible_by_400_are_leap_years(self):
        """Règle 1 : Les années divisibles par 400 sont bissextiles."""
        self.assertTrue(is_leap_year(2000))
        self.assertTrue(is_leap_year(1600))
        self.assertTrue(is_leap_year(2400))

    def test_divisible_by_100_but_not_400_are_not_leap_years(self):
        """Règle 2 : Les années divisibles par 100 mais pas par 400 ne sont pas bissextiles."""
        self.assertFalse(is_leap_year(1700))
        self.assertFalse(is_leap_year(1800))
        self.assertFalse(is_leap_year(1900))
        self.assertFalse(is_leap_year(2100))

    def test_divisible_by_4_but_not_100_are_leap_years(self):
        """Règle 3 : Les années divisibles par 4 mais pas par 100 sont bissextiles."""
        self.assertTrue(is_leap_year(2008))
        self.assertTrue(is_leap_year(2012))
        self.assertTrue(is_leap_year(2016))

    def test_not_divisible_by_4_are_not_leap_years(self):
        """Règle 4 : Les années non divisibles par 4 ne sont pas bissextiles."""
        self.assertFalse(is_leap_year(2017))
        self.assertFalse(is_leap_year(2018))
        self.assertFalse(is_leap_year(2019))
        self.assertFalse(is_leap_year(2021))


if __name__ == '__main__':
    unittest.main()