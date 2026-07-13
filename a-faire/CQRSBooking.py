import unittest
from dataclasses import dataclass
from datetime import date, timedelta
from typing import List, Dict, Tuple

"""
KATA CQRS BOOKING (Réservation d'hôtel)

Description du problème :
Vous devez implémenter une solution simple de réservation en utilisant l'architecture CQRS.
- CQRS signifie "Command Query Responsibility Segregation" (Séparation des responsabilités 
  entre Commandes et Requêtes).
- Une requête (Query) renvoie des données et ne modifie pas l'état de l'objet.
- Une commande (Command) modifie l'état d'un objet mais ne renvoie aucune donnée.
- Le code doit être divisé en lecture et écriture pour appliquer ce patron de conception.

Sujet de réservation :
Nous voulons créer une solution de réservation pour un hôtel. Les 2 premières User Stories sont :
1. En tant qu'utilisateur, je veux voir toutes les chambres libres.
2. En tant qu'utilisateur, je veux réserver une chambre.

Pour appliquer le pattern CQRS, nous aurons :
- Un Command Service avec une fonction `reserver_chambre(reservation)`
    - qui appelle le `WriteRegistry`
    - qui notifie le `ReadRegistry` (utilisé par le Query Service)
- Un Query Service avec une fonction `chambres_libres(arrivee: Date, depart: Date) -> Liste[Chambre]`

Structures de données :
- `Reservation` contient : client_id, nom_chambre, date_arrivee, date_depart
- `Chambre` contient uniquement : nom
"""

# --- MODÈLES DE DONNÉES (DOMAINE) ---

@dataclass
class Chambre:
    nom: str

@dataclass
class Reservation:
    client_id: str
    nom_chambre: str
    date_arrivee: date
    date_depart: date


# --- CÔTÉ LECTURE (QUERIES) ---

class ReadRegistry:
    """
    Le registre de lecture maintient un état optimisé pour la consultation.
    Ici, il garde une trace des périodes d'indisponibilité pour chaque chambre.
    """
    def __init__(self, chambres: List[Chambre]):
        self.chambres = chambres
        # Dictionnaire associant le nom d'une chambre à ses périodes de réservation
        self.indisponibilites: Dict[str, List[Tuple[date, date]]] = {c.nom: [] for c in chambres}

    def synchroniser_nouvelle_reservation(self, nom_chambre: str, arrivee: date, depart: date) -> None:
        """Met à jour le modèle de lecture (appelé après une commande réussie)."""
        if nom_chambre in self.indisponibilites:
            self.indisponibilites[nom_chambre].append((arrivee, depart))

    def obtenir_chambres_libres(self, arrivee: date, depart: date) -> List[Chambre]:
        chambres_libres = []
        for chambre in self.chambres:
            est_libre = True
            for res_arrivee, res_depart in self.indisponibilites[chambre.nom]:
                # S'il y a un chevauchement entre les dates demandées et une réservation existante
                if not (depart <= res_arrivee or arrivee >= res_depart):
                    est_libre = False
                    break
            
            if est_libre:
                chambres_libres.append(chambre)
                
        return chambres_libres

class QueryService:
    """Service dédié uniquement à la lecture des données."""
    def __init__(self, registry: ReadRegistry):
        self._registry = registry

    def chambres_libres(self, arrivee: date, depart: date) -> List[Chambre]:
        # Une requête retourne des données sans modifier l'état.
        return self._registry.obtenir_chambres_libres(arrivee, depart)


# --- CÔTÉ ÉCRITURE (COMMANDS) ---

class WriteRegistry:
    """Le registre d'écriture stocke la source de vérité des commandes appliquées."""
    def __init__(self):
        self.reservations: List[Reservation] = []

    def enregistrer(self, reservation: Reservation) -> None:
        self.reservations.append(reservation)

class CommandService:
    """Service dédié uniquement à l'exécution des actions et à la modification de l'état."""
    def __init__(self, write_registry: WriteRegistry, read_registry: ReadRegistry):
        self._write_registry = write_registry
        self._read_registry = read_registry

    def reserver_chambre(self, reservation: Reservation) -> None:
        # 1. Traitement métier et sauvegarde dans la base d'écriture
        self._write_registry.enregistrer(reservation)
        
        # 2. Notification/Synchronisation avec la base de lecture
        self._read_registry.synchroniser_nouvelle_reservation(
            reservation.nom_chambre,
            reservation.date_arrivee,
            reservation.date_depart
        )


# --- TESTS UNITAIRES ---

class TestCQRSBooking(unittest.TestCase):
    
    def setUp(self):
        """Initialise l'environnement CQRS pour chaque test avec 3 chambres."""
        self.chambres_hotel = [Chambre("101"), Chambre("102"), Chambre("Suite 200")]
        
        # Initialisation des registres
        self.read_registry = ReadRegistry(self.chambres_hotel)
        self.write_registry = WriteRegistry()
        
        # Initialisation des services séparés
        self.query_service = QueryService(self.read_registry)
        self.command_service = CommandService(self.write_registry, self.read_registry)
        
        # Dates utilitaires pour les tests
        self.aujourd_hui = date(2023, 10, 1)
        self.demain = self.aujourd_hui + timedelta(days=1)
        self.dans_3_jours = self.aujourd_hui + timedelta(days=3)
        self.dans_5_jours = self.aujourd_hui + timedelta(days=5)

    def test_voir_toutes_les_chambres_libres_initialement(self):
        """Test US1 : Au départ, toutes les chambres sont libres."""
        libres = self.query_service.chambres_libres(self.aujourd_hui, self.demain)
        
        self.assertEqual(len(libres), 3)
        self.assertEqual(libres[0].nom, "101")
        self.assertEqual(libres[1].nom, "102")
        self.assertEqual(libres[2].nom, "Suite 200")

    def test_reserver_une_chambre(self):
        """Test US2 : La réservation d'une chambre la retire des chambres libres pour ces dates."""
        reservation = Reservation("ClientA", "101", self.aujourd_hui, self.dans_3_jours)
        
        # Exécution de la commande
        self.command_service.reserver_chambre(reservation)
        
        # Exécution de la requête pour les mêmes dates
        libres = self.query_service.chambres_libres(self.aujourd_hui, self.dans_3_jours)
        
        self.assertEqual(len(libres), 2)
        noms_libres = [c.nom for c in libres]
        self.assertNotIn("101", noms_libres)
        self.assertIn("102", noms_libres)
        
        # Vérification que le WriteRegistry a bien stocké la commande
        self.assertEqual(len(self.write_registry.reservations), 1)

    def test_chambre_libre_avant_ou_apres_reservation(self):
        """Une chambre réservée redevient disponible à une autre période."""
        # Réservation de J à J+3
        reservation = Reservation("ClientA", "101", self.aujourd_hui, self.dans_3_jours)
        self.command_service.reserver_chambre(reservation)
        
        # Requête pour une période ultérieure (J+3 à J+5) - La chambre 101 doit être libre (le départ se fait le matin)
        libres_apres = self.query_service.chambres_libres(self.dans_3_jours, self.dans_5_jours)
        self.assertIn("101", [c.nom for c in libres_apres])

    def test_chevauchement_de_dates(self):
        """Vérifie qu'un chevauchement partiel rend bien la chambre indisponible."""
        reservation = Reservation("ClientA", "102", self.demain, self.dans_5_jours)
        self.command_service.reserver_chambre(reservation)
        
        # Requête qui chevauche le début de la réservation
        libres = self.query_service.chambres_libres(self.aujourd_hui, self.dans_3_jours)
        self.assertNotIn("102", [c.nom for c in libres])


if __name__ == '__main__':
    unittest.main()