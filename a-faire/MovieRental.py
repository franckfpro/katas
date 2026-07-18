"""
Kata Movie Rental (Location de films) - Consignes

Origine : 
Ce kata est tiré du célèbre livre de Martin Fowler, "Refactoring: Improving the 
Design of Existing Code". Il commence par un exemple (très) simple de code 
nécessitant un remaniement (refactoring).

Contexte :
Actuellement, le système génère un relevé de location au format texte simple.
Nous voulons écrire une nouvelle version de ce relevé au format HTML.

Objectif :
Appliquer la règle d'or du refactoring : "D'abord, refactorez le programme pour 
rendre l'ajout de la fonctionnalité facile, puis ajoutez la fonctionnalité."
Vous devez extraire la logique de calcul pour qu'elle soit réutilisable, puis 
implémenter la méthode `html_statement()`.
"""

import unittest

# ==========================================
# LOGIQUE MÉTIER (SOLUTION REFACTORISÉE)
# ==========================================

class Movie:
    REGULAR = 0
    NEW_RELEASE = 1
    CHILDRENS = 2

    def __init__(self, title: str, price_code: int):
        self.title = title
        self.price_code = price_code

    def get_charge(self, days_rented: int) -> float:
        """Calcule le prix de la location en fonction du type de film et de la durée."""
        result = 0.0
        if self.price_code == self.REGULAR:
            result += 2
            if days_rented > 2:
                result += (days_rented - 2) * 1.5
        elif self.price_code == self.NEW_RELEASE:
            result += days_rented * 3
        elif self.price_code == self.CHILDRENS:
            result += 1.5
            if days_rented > 3:
                result += (days_rented - 3) * 1.5
        return result

    def get_frequent_renter_points(self, days_rented: int) -> int:
        """Calcule les points de fidélité gagnés pour ce film."""
        # Bonus pour une nouveauté louée au moins 2 jours
        if self.price_code == self.NEW_RELEASE and days_rented > 1:
            return 2
        return 1


class Rental:
    def __init__(self, movie: Movie, days_rented: int):
        self.movie = movie
        self.days_rented = days_rented

    def get_charge(self) -> float:
        return self.movie.get_charge(self.days_rented)

    def get_frequent_renter_points(self) -> int:
        return self.movie.get_frequent_renter_points(self.days_rented)


class Customer:
    def __init__(self, name: str):
        self.name = name
        self.rentals = []

    def add_rental(self, rental: Rental):
        self.rentals.append(rental)

    def get_total_charge(self) -> float:
        return sum(rental.get_charge() for rental in self.rentals)

    def get_total_frequent_renter_points(self) -> int:
        return sum(rental.get_frequent_renter_points() for rental in self.rentals)

    def statement(self) -> str:
        """Génère le relevé de location au format texte brut."""
        result = f"Rental Record for {self.name}\n"
        
        for rental in self.rentals:
            result += f"\t{rental.movie.title}\t{rental.get_charge()}\n"
            
        result += f"Amount owed is {self.get_total_charge()}\n"
        result += f"You earned {self.get_total_frequent_renter_points()} frequent renter points"
        return result

    def html_statement(self) -> str:
        """Génère le relevé de location au format HTML (La nouvelle fonctionnalité)."""
        result = f"<h1>Rentals for <em>{self.name}</em></h1><p>\n"
        
        for rental in self.rentals:
            result += f"{rental.movie.title}: {rental.get_charge()}<br>\n"
            
        result += f"</p><p>You owe <em>{self.get_total_charge()}</em></p>\n"
        result += f"<p>On this rental you earned <em>{self.get_total_frequent_renter_points()}</em> frequent renter points</p>"
        return result


# ==========================================
# SUITE DE TESTS UNITAIRES
# ==========================================

class TestMovieRental(unittest.TestCase):
    
    def setUp(self):
        self.customer = Customer("Alice")
        self.movie_regular = Movie("Indiana Jones", Movie.REGULAR)
        self.movie_new = Movie("Dune: Part Two", Movie.NEW_RELEASE)
        self.movie_childrens = Movie("Toy Story", Movie.CHILDRENS)

    def test_regular_movie_statement(self):
        self.customer.add_rental(Rental(self.movie_regular, 3)) # 2 jours inclus + 1 jour supp = 3.5
        expected_statement = (
            "Rental Record for Alice\n"
            "\tIndiana Jones\t3.5\n"
            "Amount owed is 3.5\n"
            "You earned 1 frequent renter points"
        )
        self.assertEqual(self.customer.statement(), expected_statement)

    def test_new_release_movie_statement(self):
        self.customer.add_rental(Rental(self.movie_new, 2)) # 2 * 3 = 6.0, bonus points = 2
        expected_statement = (
            "Rental Record for Alice\n"
            "\tDune: Part Two\t6.0\n"
            "Amount owed is 6.0\n"
            "You earned 2 frequent renter points"
        )
        self.assertEqual(self.customer.statement(), expected_statement)

    def test_childrens_movie_statement(self):
        self.customer.add_rental(Rental(self.movie_childrens, 4)) # 3 jours inclus + 1 jour supp = 3.0
        expected_statement = (
            "Rental Record for Alice\n"
            "\tToy Story\t3.0\n"
            "Amount owed is 3.0\n"
            "You earned 1 frequent renter points"
        )
        self.assertEqual(self.customer.statement(), expected_statement)

    def test_multiple_rentals_html_statement(self):
        self.customer.add_rental(Rental(self.movie_regular, 1))
        self.customer.add_rental(Rental(self.movie_new, 3))
        self.customer.add_rental(Rental(self.movie_childrens, 3))
        
        # Regular (1 day) = 2.0
        # New (3 days) = 9.0
        # Childrens (3 days) = 1.5
        # Total = 12.5 | Points = 1 + 2 + 1 = 4
        
        expected_html = (
            "<h1>Rentals for <em>Alice</em></h1><p>\n"
            "Indiana Jones: 2.0<br>\n"
            "Dune: Part Two: 9.0<br>\n"
            "Toy Story: 1.5<br>\n"
            "</p><p>You owe <em>12.5</em></p>\n"
            "<p>On this rental you earned <em>4</em> frequent renter points</p>"
        )
        self.assertEqual(self.customer.html_statement(), expected_html)


if __name__ == '__main__':
    unittest.main()