"""
================================================================================
KATA ORM - TRADUCTION ET ADAPTATION PYTHON
================================================================================

CONSIGNES :

1. MÊME OBJET EN BASE ET EN MÉTIER (Étape initiale)
   Écrivez un programme de contacts qui utilise un ORM pour lire et écrire 
   des Personnes (Person) dans une base de données sqlite3.
   Une personne possède 3 attributs :
   - Name (Nom)
   - Surname (Prénom)
   - Birth date (Date de naissance)

2. BASE DE DONNÉES DE TEST ET DE PRODUCTION
   Nous voulons avoir une base de test nommée `tests.db` et une base de 
   production définie par la variable d'environnement `DB_URL`.
   En production, la base de données contient initialement ces contacts :
   - Elon Musk: June 28, 1971
   - Kamala Harris: October 20, 1964
   - Joe Biden: November 20, 1942
   - (etc.)

3. VERSION DU SCHÉMA ET MIGRATION
   Ajoutez une version de schéma dans votre code et votre base de données.
   Ajoutez l'attribut `email` et gérez la migration en production :
   - Si la version du code est inférieure à celle de la DB : annuler la migration (down).
   - Si la version du code est supérieure à celle de la DB : appliquer la migration (up).

4. UN OBJET POUR LA BASE ET UN POUR LE MÉTIER
   Ajoutez un Objet Valeur métier `Person` qui possède un attribut `address` avec ces règles :
   - Dans l'objet métier, `address` ne contient QUE la dernière adresse connue.
   - En base de données, on conserve l'HISTORIQUE des adresses via une nouvelle 
     table contenant (person_id, creation_date, address).

5. POUR ALLER PLUS LOIN (À implémenter lors de vos prochaines itérations TDD) :
   - Relation 1-to-1 : Identifiant National (Genre, Année, Mois, Ville, Rang, Clé).
   - Relation 1-to-Many : Collection de numéros de téléphone.
   - Relation Many-to-Many : 2 parents et 0 ou plusieurs enfants.
   - Héritage : Étudiant (université, diplôme) et Employé (bureau, embauche, salaire).
   - Base de production : Remplacer SQLite par PostgreSQL ou MySQL.

================================================================================
"""

import os
import sqlite3
import unittest
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

# ==============================================================================
# COUCHE MÉTIER (BUSINESS LAYER)
# ==============================================================================

@dataclass
class Person:
    """Objet Métier (Business Object)"""
    name: str
    surname: str
    birth_date: datetime
    email: Optional[str] = None
    address: Optional[str] = None  # Ne contient que la dernière adresse
    id: Optional[int] = None


# ==============================================================================
# COUCHE ACCÈS AUX DONNÉES (MICRO-ORM & REPOSITORY)
# ==============================================================================

class DatabaseManager:
    """Gère la connexion selon l'environnement (Test vs Prod) et les migrations."""
    
    CURRENT_SCHEMA_VERSION = 2  # V1: Personnes, V2: Ajout Email + Adresses

    def __init__(self, force_test_db=False):
        if force_test_db:
            self.db_path = "tests.db"
        else:
            self.db_path = os.environ.get("DB_URL", "production.db")
            
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._ensure_schema()

    def _ensure_schema(self):
        cursor = self.conn.cursor()
        # Table de gestion des versions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schema_info (
                version INTEGER PRIMARY KEY
            )
        """)
        
        cursor.execute("SELECT MAX(version) as v FROM schema_info")
        row = cursor.fetchone()
        db_version = row['v'] if row and row['v'] else 0

        # MIGRATIONS (Up)
        if db_version < 1:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS persons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    surname TEXT,
                    birth_date DATE
                )
            """)
            cursor.execute("INSERT INTO schema_info (version) VALUES (1)")
            db_version = 1

        if db_version < 2 and self.CURRENT_SCHEMA_VERSION >= 2:
            cursor.execute("ALTER TABLE persons ADD COLUMN email TEXT")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS addresses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    person_id INTEGER,
                    creation_date DATETIME,
                    address TEXT,
                    FOREIGN KEY(person_id) REFERENCES persons(id)
                )
            """)
            cursor.execute("INSERT INTO schema_info (version) VALUES (2)")
            db_version = 2
            
        self.conn.commit()

    def close(self):
        self.conn.close()


class PersonRepository:
    """Fait le pont entre l'Objet Métier et la Base de Données."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def save(self, person: Person) -> Person:
        cursor = self.db.conn.cursor()
        
        # 1. Sauvegarde de la personne
        if person.id is None:
            cursor.execute(
                "INSERT INTO persons (name, surname, birth_date, email) VALUES (?, ?, ?, ?)",
                (person.name, person.surname, person.birth_date.strftime("%Y-%m-%d"), person.email)
            )
            person.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE persons SET name=?, surname=?, birth_date=?, email=? WHERE id=?",
                (person.name, person.surname, person.birth_date.strftime("%Y-%m-%d"), person.email, person.id)
            )
            
        # 2. Sauvegarde de l'adresse (Historisation en base)
        if person.address:
            # Vérifier si c'est une nouvelle adresse par rapport à la dernière connue
            cursor.execute(
                "SELECT address FROM addresses WHERE person_id=? ORDER BY creation_date DESC LIMIT 1", 
                (person.id,)
            )
            last_address_row = cursor.fetchone()
            
            if not last_address_row or last_address_row['address'] != person.address:
                cursor.execute(
                    "INSERT INTO addresses (person_id, creation_date, address) VALUES (?, ?, ?)",
                    (person.id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), person.address)
                )
                
        self.db.conn.commit()
        return person

    def get_by_id(self, person_id: int) -> Optional[Person]:
        cursor = self.db.conn.cursor()
        
        # Récupération des infos de base
        cursor.execute("SELECT * FROM persons WHERE id=?", (person_id,))
        row = cursor.fetchone()
        if not row:
            return None
            
        # Récupération exclusive de la DERNIÈRE adresse pour l'objet métier
        cursor.execute(
            "SELECT address FROM addresses WHERE person_id=? ORDER BY creation_date DESC LIMIT 1", 
            (person_id,)
        )
        address_row = cursor.fetchone()
        latest_address = address_row['address'] if address_row else None
        
        return Person(
            id=row['id'],
            name=row['name'],
            surname=row['surname'],
            birth_date=datetime.strptime(row['birth_date'], "%Y-%m-%d"),
            email=row.keys().count('email') and row['email'] or None,
            address=latest_address
        )


# ==============================================================================
# TESTS UNITAIRES
# ==============================================================================

class TestORMKata(unittest.TestCase):
    
    def setUp(self):
        # On force la base de données de test
        self.db_manager = DatabaseManager(force_test_db=True)
        self.repo = PersonRepository(self.db_manager)
        
        # Nettoyage de la base de test avant chaque test
        cursor = self.db_manager.conn.cursor()
        cursor.execute("DELETE FROM addresses")
        cursor.execute("DELETE FROM persons")
        self.db_manager.conn.commit()

    def tearDown(self):
        self.db_manager.close()
        if os.path.exists("tests.db"):
            os.remove("tests.db")

    def test_database_routing(self):
        """Valide la séparation entre la base de test et la production."""
        test_db = DatabaseManager(force_test_db=True)
        self.assertEqual(test_db.db_path, "tests.db")
        
        # Simulation d'un environnement de production
        os.environ["DB_URL"] = "my_prod_database.db"
        prod_db = DatabaseManager(force_test_db=False)
        self.assertEqual(prod_db.db_path, "my_prod_database.db")
        
        # Nettoyage du fichier prod de test
        prod_db.close()
        if os.path.exists("my_prod_database.db"):
            os.remove("my_prod_database.db")

    def test_save_and_retrieve_person(self):
        """Valide la persistance basique d'une Personne avec le nouveau champ email."""
        p = Person(
            name="Musk",
            surname="Elon",
            birth_date=datetime(1971, 6, 28),
            email="elon@spacex.com"
        )
        saved_person = self.repo.save(p)
        self.assertIsNotNone(saved_person.id)
        
        retrieved = self.repo.get_by_id(saved_person.id)
        self.assertEqual(retrieved.name, "Musk")
        self.assertEqual(retrieved.email, "elon@spacex.com")

    def test_address_history_logic(self):
        """
        Valide la séparation DB/Métier : 
        L'objet métier ne voit que la dernière adresse, la base garde l'historique.
        """
        p = Person(
            name="Biden",
            surname="Joe",
            birth_date=datetime(1942, 11, 20),
            address="Delaware"
        )
        saved_person = self.repo.save(p)
        
        # Déménagement
        saved_person.address = "White House, Washington DC"
        self.repo.save(saved_person)
        
        # Récupération via le repository métier
        retrieved = self.repo.get_by_id(saved_person.id)
        
        # 1. Vérification côté Métier : une seule adresse (la dernière)
        self.assertEqual(retrieved.address, "White House, Washington DC")
        
        # 2. Vérification côté DB : l'historique complet doit être présent
        cursor = self.db_manager.conn.cursor()
        cursor.execute("SELECT address FROM addresses WHERE person_id=? ORDER BY creation_date ASC", (saved_person.id,))
        addresses_in_db = [row['address'] for row in cursor.fetchall()]
        
        self.assertEqual(len(addresses_in_db), 2)
        self.assertEqual(addresses_in_db[0], "Delaware")
        self.assertEqual(addresses_in_db[1], "White House, Washington DC")

if __name__ == '__main__':
    unittest.main(verbosity=2)