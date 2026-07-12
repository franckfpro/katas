import unittest
from typing import TypeVar, Generic, List

"""
KATA COLLECTION DEFAULT ITEM (ÉLÉMENT PAR DÉFAUT D'UNE COLLECTION)

Description du problème :
Vous devez ajouter la prise en charge d'albums photos pour une application. 
Pour cet exercice, une "Photo" peut être modélisée par une simple URI unique (chaîne de caractères). 

Règles (Partie 1) :
- Un album photo doit contenir au moins une photo.
- Il doit toujours posséder une "photo de couverture" (l'élément par défaut) parmi les photos de l'album.
- Vous devez pouvoir : créer un album, ajouter des photos, supprimer des photos, 
  et choisir la photo de couverture.
- Réfléchissez à la gestion des états invalides : 
  Que se passe-t-il si on supprime la photo de couverture ? 
  Comment empêcher d'avoir un album sans photo ?

Abstraction (Partie 2) :
- Abstrayez votre implémentation pour qu'elle fonctionne avec n'importe quel type de données.
- Par exemple, au lieu d'un "album de photos" avec une "photo de couverture", 
  elle doit pouvoir gérer un "carnet d'adresses client" avec une "adresse par défaut".
- Utilisez les types génériques (Generics) pour rendre votre conception réutilisable.
"""

# --- EXCEPTIONS PERSONNALISÉES ---

class ErreurCollectionVide(Exception):
    """Levée lorsqu'on tente de supprimer le dernier élément de la collection."""
    pass

class ErreurElementInconnu(Exception):
    """Levée lorsqu'on tente d'interagir avec un élément absent de la collection."""
    pass


# --- IMPLÉMENTATION MÉTIER (PARTIE 1 & 2) ---

T = TypeVar('T') # Permet de rendre la classe générique pour n'importe quel type

class CollectionAvecDefaut(Generic[T]):
    def __init__(self, element_initial: T):
        """
        Garantit que la collection n'est jamais vide à sa création 
        et possède toujours un élément par défaut.
        """
        self._elements: List[T] = [element_initial]
        self._defaut: T = element_initial

    @property
    def elements(self) -> List[T]:
        """Retourne une copie de la liste pour éviter la modification depuis l'extérieur."""
        return list(self._elements)

    @property
    def defaut(self) -> T:
        """Retourne l'élément par défaut actuel."""
        return self._defaut

    def ajouter(self, element: T) -> None:
        """Ajoute un élément s'il n'est pas déjà présent."""
        if element not in self._elements:
            self._elements.append(element)

    def definir_defaut(self, element: T) -> None:
        """Modifie l'élément par défaut (doit être présent dans la collection)."""
        if element not in self._elements:
            raise ErreurElementInconnu("Impossible de définir comme défaut un élément absent de la collection.")
        self._defaut = element

    def supprimer(self, element: T) -> None:
        """
        Supprime un élément. 
        Gère la protection contre la suppression du dernier élément et 
        la réassignation automatique de l'élément par défaut si nécessaire.
        """
        if element not in self._elements:
            raise ErreurElementInconnu("L'élément n'est pas dans la collection.")
        
        if len(self._elements) == 1:
            raise ErreurCollectionVide("La collection doit contenir au moins un élément.")
        
        self._elements.remove(element)
        
        # Si on vient de supprimer l'élément par défaut, on en assigne un nouveau (le premier disponible)
        if self._defaut == element:
            self._defaut = self._elements[0]


# --- TESTS UNITAIRES ---

class TestCollectionAvecDefaut(unittest.TestCase):

    def test_creation_collection_initialise_defaut(self):
        """L'élément initial devient automatiquement le défaut."""
        album = CollectionAvecDefaut[str]("http://mon-site.com/photo1.jpg")
        self.assertEqual(album.defaut, "http://mon-site.com/photo1.jpg")
        self.assertEqual(len(album.elements), 1)

    def test_ajouter_nouvel_element(self):
        """On peut ajouter de nouveaux éléments sans altérer le défaut."""
        album = CollectionAvecDefaut[str]("photo1.jpg")
        album.ajouter("photo2.jpg")
        self.assertIn("photo2.jpg", album.elements)
        self.assertEqual(album.defaut, "photo1.jpg")

    def test_definir_nouveau_defaut(self):
        """On peut changer le défaut pour un autre élément existant."""
        album = CollectionAvecDefaut[str]("photo1.jpg")
        album.ajouter("photo2.jpg")
        album.definir_defaut("photo2.jpg")
        self.assertEqual(album.defaut, "photo2.jpg")

    def test_erreur_definir_defaut_inconnu(self):
        """Définir un défaut avec un élément qui n'est pas dans la collection lève une erreur."""
        album = CollectionAvecDefaut[str]("photo1.jpg")
        with self.assertRaises(ErreurElementInconnu):
            album.definir_defaut("photo_inconnue.jpg")

    def test_supprimer_element_non_defaut(self):
        """Supprimer un élément standard fonctionne et ne touche pas au défaut."""
        album = CollectionAvecDefaut[str]("photo1.jpg")
        album.ajouter("photo2.jpg")
        album.supprimer("photo2.jpg")
        self.assertEqual(len(album.elements), 1)
        self.assertEqual(album.defaut, "photo1.jpg")

    def test_supprimer_element_defaut_reassigne_automatiquement(self):
        """Supprimer le défaut actuel réassigne le défaut au premier élément restant."""
        album = CollectionAvecDefaut[str]("photo1.jpg")
        album.ajouter("photo2.jpg")
        album.supprimer("photo1.jpg")
        self.assertEqual(album.defaut, "photo2.jpg")

    def test_erreur_supprimer_dernier_element(self):
        """Il est interdit de vider la collection."""
        album = CollectionAvecDefaut[str]("photo1.jpg")
        with self.assertRaises(ErreurCollectionVide):
            album.supprimer("photo1.jpg")

    def test_reutilisabilite_avec_autre_type_donnees(self):
        """Test de la Partie 2 : utilisation avec un dictionnaire (ex: adresses client)."""
        adresse_domicile = {"rue": "123 Rue de Paris", "type": "domicile"}
        adresse_travail = {"rue": "456 Tour Business", "type": "travail"}
        
        carnet_adresses = CollectionAvecDefaut[dict](adresse_domicile)
        carnet_adresses.ajouter(adresse_travail)
        carnet_adresses.definir_defaut(adresse_travail)
        
        self.assertEqual(carnet_adresses.defaut["type"], "travail")


if __name__ == '__main__':
    unittest.main()