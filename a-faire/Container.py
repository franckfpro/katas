import unittest
import inspect
from abc import ABC, abstractmethod

"""
KATA DI CONTAINER (Conteneur d'Injection de Dépendances)

Description du problème :
Construire un conteneur d'injection de dépendances (DI) simple est un excellent moyen 
d'améliorer votre compréhension de l'inversion de contrôle, de l'analyse dynamique 
(réflexion/introspection) et du typage.

Dans ce kata, vous devez faire passer une série de tests qui démontrent que votre 
conteneur répond aux exigences. Écrivez (ou dé-commentez) chaque test un par un, 
puis implémentez la logique nécessaire dans le conteneur pour faire réussir le test. 
Refactorez après chaque étape. Vous êtes libre de donner au conteneur l'API que 
vous préférez ou de vous en tenir aux méthodes suggérées : `register` et `resolve`.

En général, il y a 3 étapes impliquées dans l'utilisation du conteneur :
1. Créer une instance du conteneur.
2. Enregistrer un (ou plusieurs) types (Associer une Interface à une Implémentation).
3. Résoudre un type (Demander au conteneur de créer l'instance avec ses dépendances).

Exigences (Tests) adaptées pour Python :
1. `resolve` retourne une instance d'une classe simple (sans constructeur complexe).
2. `resolve` retourne une instance d'un type qui implémente une interface (Classe abstraite) 
   en utilisant un constructeur sans paramètre.
3. `resolve` lève une exception descriptive lors de la tentative de résolution d'un type 
   pour lequel rien n'a été enregistré.
4. `resolve` retourne l'instance d'une classe qui nécessite une autre classe comme paramètre 
   de son constructeur (Injection de dépendance de niveau 1).
5. `resolve` gère les dépendances imbriquées (Une classe A dépend d'une interface B, 
   dont l'implémentation dépend d'une classe C).
   
Ressources Python :
- Le module `inspect` (spécialement `inspect.signature`)
- Le module `typing` et les annotations de type.
"""

# --- EXCEPTIONS PERSONNALISÉES ---

class ErreurResolutionDependance(Exception):
    """Levée lorsqu'une dépendance ne peut pas être résolue ou n'est pas enregistrée."""
    pass


# --- IMPLÉMENTATION DU CONTENEUR ---

class DIContainer:
    def __init__(self):
        self._registre = {}

    def register(self, interface, implementation=None):
        """
        Enregistre un type dans le conteneur.
        Si l'implémentation n'est pas fournie, on considère que l'interface 
        s'enregistre elle-même.
        """
        if implementation is None:
            implementation = interface
        self._registre[interface] = implementation

    def resolve(self, interface):
        """
        Résout une interface en instanciant l'implémentation associée et 
        en injectant automatiquement ses dépendances.
        """
        if interface not in self._registre:
            raise ErreurResolutionDependance(
                f"Échec de la résolution : Le type '{interface.__name__}' n'est pas enregistré dans le conteneur."
            )
        
        implementation = self._registre[interface]
        
        # Récupération de la signature du constructeur (__init__)
        try:
            signature = inspect.signature(implementation.__init__)
        except TypeError:
            # Gère le cas des classes intégrées ou sans __init__ redéfini
            return implementation()

        parametres = signature.parameters
        dependances = {}
        
        for nom, param in parametres.items():
            # On ignore 'self' ou '*args', '**kwargs' pour cet exercice basique
            if nom == 'self' or param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue
                
            # Si le paramètre n'a pas d'annotation de type, on ne sait pas quoi injecter
            if param.annotation == inspect.Parameter.empty:
                raise ErreurResolutionDependance(
                    f"Impossible d'injecter '{nom}' dans '{implementation.__name__}' : "
                    "Il manque l'annotation de type dans le constructeur."
                )
                
            # Appel récursif pour résoudre la dépendance
            dependances[nom] = self.resolve(param.annotation)
            
        # Instanciation de la classe avec ses dépendances "unpackées"
        return implementation(**dependances)


# --- DÉCLARATION DES CLASSES ET INTERFACES POUR LES TESTS ---

class ServiceSimple:
    def dis_bonjour(self):
        return "Bonjour"

class IService(ABC):
    @abstractmethod
    def executer(self):
        pass

class ServiceImplementation(IService):
    def executer(self):
        return "Exécution terminée"

class ReferentielDonnees:
    def __init__(self):
        self.donnees = [1, 2, 3]

class GestionnaireUtilisateur:
    # L'annotation de type (: ReferentielDonnees) est cruciale pour que le conteneur lise la dépendance
    def __init__(self, referentiel: ReferentielDonnees):
        self.referentiel = referentiel

class ILogger(ABC):
    @abstractmethod
    def log(self, message): pass

class ConsoleLogger(ILogger):
    def log(self, message):
        return f"LOG: {message}"

class ApplicationApp:
    # Dépendance imbriquée : ApplicationApp dépend d'un service (qui lui-même peut avoir des dépendances) 
    # et d'un logger
    def __init__(self, service: IService, logger: ILogger):
        self.service = service
        self.logger = logger
        
    def demarrer(self):
        resultat = self.service.executer()
        return self.logger.log(resultat)


# --- TESTS UNITAIRES ---

class TestDIContainer(unittest.TestCase):
    
    def setUp(self):
        self.container = DIContainer()

    def test_req1_resolution_type_simple(self):
        """1. Resolve retourne un type simple en utilisant son constructeur sans paramètre."""
        self.container.register(ServiceSimple)
        
        instance = self.container.resolve(ServiceSimple)
        
        self.assertIsInstance(instance, ServiceSimple)
        self.assertEqual(instance.dis_bonjour(), "Bonjour")

    def test_req2_resolution_interface_vers_implementation(self):
        """2. Resolve retourne une instance d'un type qui implémente une interface."""
        self.container.register(IService, ServiceImplementation)
        
        instance = self.container.resolve(IService)
        
        self.assertIsInstance(instance, ServiceImplementation)
        self.assertEqual(instance.executer(), "Exécution terminée")

    def test_req3_erreur_si_non_enregistre(self):
        """3. Resolve lève une exception descriptive si le type n'a pas été enregistré."""
        with self.assertRaisesRegex(ErreurResolutionDependance, "n'est pas enregistré dans le conteneur"):
            self.container.resolve(ServiceSimple)

    def test_req4_injection_dependance_un_niveau(self):
        """4. Resolve injecte correctement une dépendance requise dans le constructeur."""
        self.container.register(ReferentielDonnees)
        self.container.register(GestionnaireUtilisateur)
        
        gestionnaire = self.container.resolve(GestionnaireUtilisateur)
        
        self.assertIsInstance(gestionnaire, GestionnaireUtilisateur)
        self.assertIsInstance(gestionnaire.referentiel, ReferentielDonnees)
        self.assertEqual(gestionnaire.referentiel.donnees, [1, 2, 3])

    def test_req5_injection_dependances_imbriquees_et_interfaces(self):
        """
        (Bonus Python) 5. Resolve gère des dépendances imbriquées basées sur des interfaces.
        ApplicationApp demande IService et ILogger.
        """
        # Enregistrement des types et des implémentations cibles
        self.container.register(IService, ServiceImplementation)
        self.container.register(ILogger, ConsoleLogger)
        self.container.register(ApplicationApp)
        
        app = self.container.resolve(ApplicationApp)
        
        self.assertIsInstance(app, ApplicationApp)
        self.assertIsInstance(app.service, ServiceImplementation)
        self.assertIsInstance(app.logger, ConsoleLogger)
        self.assertEqual(app.demarrer(), "LOG: Exécution terminée")
        
    def test_erreur_si_annotation_manquante(self):
        """Vérifie que le système bloque si les annotations de type ne sont pas définies."""
        class ClasseMalCodee:
            def __init__(self, dependance_inconnue):
                self.dep = dependance_inconnue
                
        self.container.register(ClasseMalCodee)
        
        with self.assertRaisesRegex(ErreurResolutionDependance, "Il manque l'annotation de type"):
            self.container.resolve(ClasseMalCodee)


if __name__ == '__main__':
    unittest.main()