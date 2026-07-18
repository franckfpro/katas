"""
KATA : PAGINATION SEVEN

Description du problème :
La pagination se retrouve dans de nombreux sites web. La plupart du temps, 
nous retrouvons la page courante ainsi que la navigation vers la page précédente 
et suivante. Pour éviter une pagination trop verbeuse lorsque le nombre 
de pages est grand, nous utiliserons la représentation "Pagination Seven", 
qui affiche la navigation en se limitant toujours à exactement 7 entrées.

Règles de gestion :

Partie I - Pagination simple :
Si le nombre total de pages est de 7 ou moins, toutes les pages sont affichées.
La page courante est encadrée par des parenthèses.
Exemple (Page 2 sur 5) : 1 (2) 3 4 5
Exemple (Page 6 sur 7) : 1 2 3 4 5 (6) 7

Partie II - Pagination avancée (Milieu) :
Si le nombre total de pages excède 7, nous utilisons des ellipses "..." 
pour représenter les pages groupées et invisibles. 
Exemple (Page 42 sur 100) : 1 ... 41 (42) 43 ... 100
Exemple (Page 5 sur 9)    : 1 ... 4 (5) 6 ... 9

Partie III - Pagination avancée (Début) :
Parfois, nous n'avons pas besoin du premier "..." car nous sommes au début.
Exemple (Page 2 sur 9) : 1 (2) 3 4 5 ... 9
Exemple (Page 4 sur 9) : 1 2 3 (4) 5 ... 9

Partie IV - Pagination avancée (Fin) :
Cette même règle s'applique à la fin de la pagination.
Exemple (Page 8 sur 9) : 1 ... 5 6 7 (8) 9
Exemple (Page 6 sur 9) : 1 ... 5 (6) 7 8 9
"""

import unittest

def pagination_seven(current_page: int, total_pages: int) -> str:
    """
    Génère une chaîne de caractères représentant la pagination selon 
    les règles du "Pagination Seven".
    """
    if current_page < 1 or current_page > total_pages:
        raise ValueError("La page courante doit être comprise entre 1 et le nombre total de pages.")
    
    # Fonction utilitaire pour formater la page courante avec des parenthèses
    def format_page(p: int) -> str:
        return f"({p})" if p == current_page else str(p)
        
    # Partie I : 7 pages ou moins
    if total_pages <= 7:
        return " ".join(format_page(p) for p in range(1, total_pages + 1))
        
    # Partie III : Proche du début
    if current_page <= 4:
        pages = [format_page(p) for p in range(1, 6)]
        return " ".join(pages + ["...", str(total_pages)])
        
    # Partie IV : Proche de la fin
    elif current_page >= total_pages - 3:
        pages = [format_page(p) for p in range(total_pages - 4, total_pages + 1)]
        return " ".join(["1", "..."] + pages)
        
    # Partie II : Au milieu
    else:
        pages = [format_page(current_page - 1), format_page(current_page), format_page(current_page + 1)]
        return " ".join(["1", "..."] + pages + ["...", str(total_pages)])


class TestPaginationSeven(unittest.TestCase):

    def test_part_1_simple_pagination(self):
        """Test lorsque le nombre total de pages est <= 7."""
        self.assertEqual(pagination_seven(2, 5), "1 (2) 3 4 5")
        self.assertEqual(pagination_seven(6, 7), "1 2 3 4 5 (6) 7")
        self.assertEqual(pagination_seven(1, 3), "(1) 2 3")
        self.assertEqual(pagination_seven(7, 7), "1 2 3 4 5 6 (7)")

    def test_part_2_middle_pagination(self):
        """Test de la pagination au milieu avec double ellipse."""
        self.assertEqual(pagination_seven(42, 100), "1 ... 41 (42) 43 ... 100")
        self.assertEqual(pagination_seven(5, 9), "1 ... 4 (5) 6 ... 9")

    def test_part_3_beginning_pagination(self):
        """Test de la pagination au début avec une seule ellipse à la fin."""
        self.assertEqual(pagination_seven(2, 9), "1 (2) 3 4 5 ... 9")
        self.assertEqual(pagination_seven(4, 9), "1 2 3 (4) 5 ... 9")
        self.assertEqual(pagination_seven(1, 10), "(1) 2 3 4 5 ... 10")

    def test_part_4_end_pagination(self):
        """Test de la pagination à la fin avec une seule ellipse au début."""
        self.assertEqual(pagination_seven(8, 9), "1 ... 5 6 7 (8) 9")
        self.assertEqual(pagination_seven(6, 9), "1 ... 5 (6) 7 8 9")
        self.assertEqual(pagination_seven(10, 10), "1 ... 6 7 8 9 (10)")

    def test_invalid_current_page(self):
        """Test des erreurs liées aux entrées invalides."""
        with self.assertRaises(ValueError):
            pagination_seven(0, 5)
        with self.assertRaises(ValueError):
            pagination_seven(6, 5)

if __name__ == '__main__':
    unittest.main()