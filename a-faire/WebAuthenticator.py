import unittest
from unittest.mock import Mock, call

# ==============================================================================
# CONSIGNES DU KATA (Traduites en Français)
# ==============================================================================
"""
Contexte :
Dans ce Kata, vous êtes programmeur chez ABC Corp et vous créez une nouvelle 
application web à partir de zéro. L'architecte principal a commencé le travail, 
et c'est maintenant à vous de vous assurer que ces tâches sont accomplies :

  1. Permettre l'authentification via les paramètres de requête (GET ou POST)
     (ex: 'username' et 'password').
  2. Toutes les tentatives d'authentification/de connexion doivent être vérifiées 
     auprès de l'annuaire LDAP.
  3. Les connexions réussies doivent être enregistrées dans le registre de 
     Single Sign-On (SSO).

Cependant, vous n'êtes pas la seule équipe à travailler sur cette application. 
Le LDAP est géré par une autre équipe et vous disposez de l'interface 
`LdapAuthenticationGateway`. 
Le registre SSO est également écrit par une autre équipe, ce qui vous laisse 
l'interface `SingleSignOnRegistry`.

Votre travail :
Écrire un composant (WebAuthenticator) qui gère les requêtes entrantes et agit 
en fonction de la présence d'un cookie contenant un jeton SSO, ou des paramètres 
username+password. L'injection de dépendances est supposée être en place : pour 
obtenir le registre SSO ou la passerelle LDAP, vous devrez les injecter dans 
le constructeur de votre composant.
"""

# ==============================================================================
# INTERFACES FOURNIES (Mockées ou simulées par d'autres équipes)
# ==============================================================================

class LdapAuthenticationGateway:
    """Interface fournie par l'équipe LDAP."""
    def authenticate(self, username, password):
        raise NotImplementedError("Doit être implémenté/mocké")

class SingleSignOnRegistry:
    """Interface fournie par l'équipe SSO."""
    def is_valid(self, token):
        raise NotImplementedError("Doit être implémenté/mocké")
    
    def register(self, username):
        raise NotImplementedError("Doit être implémenté/mocké")

# Modèles simplifiés pour représenter la requête et la réponse HTTP
class Request:
    def __init__(self, params=None, cookies=None):
        self.params = params or {}
        self.cookies = cookies or {}

class Response:
    def __init__(self, is_authenticated=False, token=None):
        self.is_authenticated = is_authenticated
        self.token = token


# ==============================================================================
# VOTRE IMPLEMENTATION (Le Kata à résoudre)
# ==============================================================================

class WebAuthenticator:
    def __init__(self, ldap_gateway: LdapAuthenticationGateway, sso_registry: SingleSignOnRegistry):
        self.ldap_gateway = ldap_gateway
        self.sso_registry = sso_registry

    def handle(self, request: Request) -> Response:
        # 1. Vérifier s'il y a déjà un jeton SSO valide dans les cookies
        sso_token = request.cookies.get('sso_token')
        if sso_token and self.sso_registry.is_valid(sso_token):
            return Response(is_authenticated=True, token=sso_token)

        # 2. Sinon, vérifier les paramètres d'identification
        username = request.params.get('username')
        password = request.params.get('password')

        if username and password:
            # 3. Vérifier les identifiants via LDAP
            if self.ldap_gateway.authenticate(username, password):
                # 4. Enregistrer dans le registre SSO si succès
                new_token = self.sso_registry.register(username)
                return Response(is_authenticated=True, token=new_token)

        # Si aucune des méthodes ne réussit, l'utilisateur n'est pas authentifié
        return Response(is_authenticated=False)


# ==============================================================================
# TESTS UNITAIRES (Validation du comportement)
# ==============================================================================

class TestWebAuthentication(unittest.TestCase):

    def setUp(self):
        # Initialisation des Mocks pour isoler notre système
        self.mock_ldap = Mock(spec=LdapAuthenticationGateway)
        self.mock_sso = Mock(spec=SingleSignOnRegistry)
        self.authenticator = WebAuthenticator(self.mock_ldap, self.mock_sso)

    def test_should_authenticate_with_valid_sso_cookie(self):
        # Arrange
        request = Request(cookies={'sso_token': 'valid-token-123'})
        self.mock_sso.is_valid.return_value = True

        # Act
        response = self.authenticator.handle(request)

        # Assert
        self.assertTrue(response.is_authenticated)
        self.assertEqual(response.token, 'valid-token-123')
        # L'authentification LDAP ne doit pas être appelée si on a un cookie valide
        self.mock_ldap.authenticate.assert_not_called()

    def test_should_not_authenticate_with_invalid_sso_cookie_and_no_credentials(self):
        # Arrange
        request = Request(cookies={'sso_token': 'invalid-token'})
        self.mock_sso.is_valid.return_value = False

        # Act
        response = self.authenticator.handle(request)

        # Assert
        self.assertFalse(response.is_authenticated)
        self.mock_ldap.authenticate.assert_not_called()

    def test_should_authenticate_via_ldap_and_register_sso_when_credentials_are_valid(self):
        # Arrange
        request = Request(params={'username': 'jdoe', 'password': 'password123'})
        self.mock_ldap.authenticate.return_value = True
        self.mock_sso.register.return_value = 'new-sso-token-456'

        # Act
        response = self.authenticator.handle(request)

        # Assert
        self.assertTrue(response.is_authenticated)
        self.assertEqual(response.token, 'new-sso-token-456')
        
        # Vérification des interactions (Mocking pur)
        self.mock_ldap.authenticate.assert_called_once_with('jdoe', 'password123')
        self.mock_sso.register.assert_called_once_with('jdoe')

    def test_should_fail_authentication_when_ldap_rejects_credentials(self):
        # Arrange
        request = Request(params={'username': 'jdoe', 'password': 'wrong-password'})
        self.mock_ldap.authenticate.return_value = False

        # Act
        response = self.authenticator.handle(request)

        # Assert
        self.assertFalse(response.is_authenticated)
        # Le système ne doit PAS essayer de l'enregistrer dans le SSO si le LDAP échoue
        self.mock_sso.register.assert_not_called()

    def test_should_fallback_to_credentials_if_sso_cookie_is_invalid(self):
        # Arrange
        request = Request(
            cookies={'sso_token': 'expired-token'},
            params={'username': 'jdoe', 'password': 'password123'}
        )
        self.mock_sso.is_valid.return_value = False
        self.mock_ldap.authenticate.return_value = True
        self.mock_sso.register.return_value = 'refreshed-sso-token'

        # Act
        response = self.authenticator.handle(request)

        # Assert
        self.assertTrue(response.is_authenticated)
        self.assertEqual(response.token, 'refreshed-sso-token')
        self.mock_ldap.authenticate.assert_called_once_with('jdoe', 'password123')

if __name__ == '__main__':
    unittest.main()