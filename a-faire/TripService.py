"""
======================================================================
KATA : TRIP SERVICE
======================================================================

CONSIGNES :
Kata pour une session pratique sur du code legacy (existant).
L'objectif est de tester et refactoriser la classe legacy TripService. 
Le résultat final doit être un code bien conçu qui exprime le domaine.

Contraintes du Legacy :
- TripDAO communique avec la base de données. Si vous l'appelez dans un test, 
  il lève une exception.
- UserSession communique avec le système web/réseau. Si vous l'appelez 
  dans un test, il lève également une exception.

Votre mission :
1. Écrire des tests unitaires pour `get_trips_by_user` en trouvant un moyen
   de contourner (mocker/stubber) les dépendances dures (TripDAO et UserSession).
2. Refactoriser `get_trips_by_user` pour la rendre lisible, propre, et 
   orientée objet. Ne modifiez pas le code de production s'il n'est pas 
   couvert par un test !
======================================================================
"""

import unittest

# --- EXCEPTION ---
class UserNotLoggedInException(Exception):
    pass


# --- ENTITÉS DU DOMAINE ---
class Trip:
    pass


class User:
    def __init__(self):
        self.trips = []
        self.friends = []

    def get_friends(self):
        return self.friends

    def add_friend(self, friend):
        self.friends.append(friend)

    def get_trips(self):
        return self.trips

    def add_trip(self, trip):
        self.trips.append(trip)


# --- DÉPENDANCES EXTERNES (Gênantes pour les tests) ---
class UserSession:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(UserSession, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def get_logged_user(self):
        # Simule un appel réseau qui plante en environnement de test
        raise Exception("UserSession.get_logged_user() ne doit pas être appelé dans un test unitaire !")


class TripDAO:
    @staticmethod
    def find_trips_by_user(user):
        # Simule un appel base de données qui plante en environnement de test
        raise Exception("TripDAO ne doit pas être invoqué dans un test unitaire !")


# --- CODE LEGACY À TESTER ET REFACTORISER ---
class TripService:
    def get_trips_by_user(self, user):
        trip_list = []
        logged_user = UserSession.get_instance().get_logged_user()
        is_friend = False
        
        if logged_user is not None:
            for friend in user.get_friends():
                if friend == logged_user:
                    is_friend = True
                    break
            
            if is_friend:
                trip_list = TripDAO.find_trips_by_user(user)
            
            return trip_list
        else:
            raise UserNotLoggedInException()


# ======================================================================
# ZONE DE TESTS UNITAIRES
# ======================================================================
class TestTripService(unittest.TestCase):
    
    def setUp(self):
        self.trip_service = TripService()

    def test_should_throw_exception_when_user_is_not_logged_in(self):
        # TODO: Implémenter le test. 
        # Astuce : vous allez devoir extraire l'appel à UserSession 
        # dans une méthode protégée pour pouvoir la surcharger ici.
        pass

    # Ajoutez vos autres tests ici...
    # - Que se passe-t-il si les utilisateurs ne sont pas amis ?
    # - Que se passe-t-il si les utilisateurs sont amis ?

if __name__ == '__main__':
    unittest.main()