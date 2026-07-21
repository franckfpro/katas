import unittest
from dataclasses import dataclass
from typing import List

# ==============================================================================
# CONSIGNES DU KATA (Traduites en Français)
# ==============================================================================
"""
À propos de ce Kata :
Ce Kata a été développé pour montrer comment la sur-spécification des assertions 
nuit à la maintenabilité des tests. 

Description du problème :
Vous construisez un système de gestion des employés pour une épicerie locale. 
Le propriétaire souhaite ouvrir le magasin le dimanche, mais en raison de 
restrictions légales, les employés de moins de 18 ans ne sont pas autorisés 
à travailler le dimanche. Le propriétaire demande une fonctionnalité de rapport 
pour pouvoir planifier les quarts de travail. 

Tous les employés sont déjà stockés quelque part et ont les propriétés suivantes :
  - name (nom) : chaîne de caractères (string)
  - age : nombre entier (int)

Règles (User Stories) :
Commencez par la première User Story et écrivez au moins un test pour chaque 
exigence. Essayez de ne pas regarder les exigences futures à l'avance et suivez 
strictement le cycle TDD.

  1. En tant que propriétaire du magasin, je veux voir une liste de tous les 
     employés âgés de 18 ans ou plus afin de savoir qui est autorisé à travailler 
     le dimanche.
  2. En tant que propriétaire du magasin, je veux que la liste des employés 
     soit triée par leur nom, afin de pouvoir les trouver plus facilement.
  3. En tant que propriétaire du magasin, je veux que les noms de la liste des 
     employés soient mis en majuscules, afin de pouvoir mieux la lire.
  4. En tant que propriétaire du magasin, je veux que les employés soient triés 
     par leur nom par ordre décroissant au lieu de croissant.
"""

# ==============================================================================
# VOTRE IMPLEMENTATION (Le Kata à résoudre)
# ==============================================================================

@dataclass
class Employee:
    """Modèle représentant un employé."""
    name: str
    age: int


def get_sunday_employees(employees: List[Employee]) -> List[Employee]:
    """
    Génère le rapport des employés autorisés à travailler le dimanche,
    en appliquant les règles métier (âge >= 18, noms en majuscules, 
    tri décroissant par nom).
    """
    # Étape 1 & 3 : Filtrer les employés majeurs et mettre leurs noms en majuscules.
    # On crée une nouvelle instance d'Employee pour conserver la pureté de la fonction 
    # et éviter d'altérer les objets originaux par effet de bord.
    allowed_employees = [
        Employee(name=emp.name.upper(), age=emp.age) 
        for emp in employees 
        if emp.age >= 18
    ]
    
    # Étape 2 & 4 : Trier la liste par ordre alphabétique décroissant.
    return sorted(allowed_employees, key=lambda e: e.name, reverse=True)


# ==============================================================================
# TESTS UNITAIRES (Validation du comportement)
# ==============================================================================

class TestEmployeeReport(unittest.TestCase):

    def setUp(self):
        # Jeu de données initial utilisé pour les tests
        self.employees = [
            Employee(name="Seiya", age=17),
            Employee(name="Shiryu", age=18),
            Employee(name="Hyoga", age=19),
            Employee(name="Shun", age=16),
            Employee(name="Ikki", age=20)
        ]

    def test_should_only_return_employees_18_or_older(self):
        """User Story 1 : Garder uniquement les employés de 18 ans et plus."""
        result = get_sunday_employees(self.employees)
        
        # Vérifie que seuls Shiryu, Hyoga et Ikki (18, 19, 20) sont conservés
        self.assertEqual(len(result), 3)
        ages = [emp.age for emp in result]
        self.assertTrue(all(age >= 18 for age in ages))

    def test_should_return_capitalized_names(self):
        """User Story 3 : Les noms doivent être en majuscules."""
        result = get_sunday_employees(self.employees)
        
        names = [emp.name for emp in result]
        self.assertTrue(all(name.isupper() for name in names))

    def test_should_return_sorted_descending_by_name(self):
        """User Story 2 & 4 : La liste doit être triée par nom en ordre décroissant."""
        result = get_sunday_employees(self.employees)
        names = [emp.name for emp in result]
        
        # Les noms originaux éligibles sont Shiryu, Hyoga, Ikki. 
        # En majuscules : SHIRYU, HYOGA, IKKI.
        # Tri descendant attendu : SHIRYU, IKKI, HYOGA.
        expected_names = ["SHIRYU", "IKKI", "HYOGA"]
        
        self.assertEqual(names, expected_names)

    def test_should_not_mutate_original_list(self):
        """Test de robustesse : Vérifier que les objets originaux ne sont pas modifiés."""
        original_name = self.employees[1].name
        get_sunday_employees(self.employees)
        
        # Le nom original doit toujours être "Shiryu" (pas en majuscules)
        self.assertEqual(self.employees[1].name, original_name)

if __name__ == '__main__':
    unittest.main()