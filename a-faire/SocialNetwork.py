import unittest
import re

# =============================================================================
# KATA : SOCIAL NETWORK (RÉSEAU SOCIAL)
# =============================================================================
#
# CONSIGNES :
# L'idée est de construire un réseau social très léger pour s'entraîner à 
# modéliser des règles de gestion (Event Storming / Example Mapping).
#
# Les fonctionnalités attendues (Epics) :
# 1. Publication (Posting) : Thomas peut publier un message.
# 2. Lecture (Reading) : Alice peut voir tous les messages de Thomas.
# 3. Abonnement (Following) : Charlie peut s'abonner aux messages de Thomas et 
#    Alice, et voir une liste agrégée de tous ses abonnements (le "mur").
# 4. Mentions : Alice peut mentionner Charlie dans un message en utilisant 
#    "@" (ex: "@Charlie"). Le réseau doit pouvoir retrouver ces mentions.
# 5. Liens (Links) : Thomas peut partager un lien vers un message spécifique.
# 6. Messages Directs (Direct Messages) : Alice peut envoyer un message privé 
#    à Thomas, visible uniquement par eux.
# =============================================================================

class Message:
    """Représente un message sur le réseau social."""
    _id_counter = 1

    def __init__(self, author, text, is_direct=False, receiver=None):
        self.id = Message._id_counter
        Message._id_counter += 1
        self.author = author
        self.text = text
        self.is_direct = is_direct
        self.receiver = receiver

    def get_link(self):
        """Génère un lien unique vers ce message."""
        return f"https://social.net/msg/{self.id}"


class SocialNetwork:
    """Gère l'ensemble de la logique du réseau social."""
    def __init__(self):
        self.messages = []
        self.subscriptions = {}  # { 'Utilisateur': set(['Abonnement1', 'Abonnement2']) }

    def publish(self, author, text):
        """Epic 1: Publier un message public."""
        msg = Message(author, text)
        self.messages.append(msg)
        return msg

    def read_timeline(self, user):
        """Epic 2: Lire les messages publics d'un utilisateur spécifique."""
        return [msg for msg in self.messages if msg.author == user and not msg.is_direct]

    def follow(self, user, target):
        """Epic 3a: S'abonner à un utilisateur."""
        if user not in self.subscriptions:
            self.subscriptions[user] = set()
        self.subscriptions[user].add(target)

    def read_wall(self, user):
        """Epic 3b: Lire les messages agrégés des abonnements."""
        followed_users = self.subscriptions.get(user, set())
        return [msg for msg in self.messages if msg.author in followed_users and not msg.is_direct]

    def get_mentions(self, user):
        """Epic 4: Récupérer tous les messages publics mentionnant l'utilisateur."""
        mention_tag = f"@{user}"
        return [msg for msg in self.messages if mention_tag in msg.text and not msg.is_direct]

    def get_message_by_link(self, link):
        """Epic 5: Retrouver un message via son lien partagé."""
        for msg in self.messages:
            if msg.get_link() == link:
                return msg
        return None

    def send_direct_message(self, sender, receiver, text):
        """Epic 6a: Envoyer un message privé."""
        msg = Message(sender, text, is_direct=True, receiver=receiver)
        self.messages.append(msg)
        return msg

    def read_direct_messages(self, user):
        """Epic 6b: Lire ses messages privés (reçus ou envoyés)."""
        return [msg for msg in self.messages if msg.is_direct and (msg.receiver == user or msg.author == user)]


# =============================================================================
# TESTS UNITAIRES
# =============================================================================

class TestSocialNetwork(unittest.TestCase):

    def setUp(self):
        """Initialisation d'un réseau social vierge avant chaque test."""
        self.network = SocialNetwork()
        # Réinitialisation du compteur d'ID pour des tests prédictibles
        Message._id_counter = 1 

    def test_posting_and_reading(self):
        """Epics 1 & 2 : Publication et lecture de messages."""
        self.network.publish("Thomas", "Bonjour tout le monde !")
        self.network.publish("Thomas", "Il fait beau aujourd'hui.")
        
        thomas_messages = self.network.read_timeline("Thomas")
        self.assertEqual(len(thomas_messages), 2)
        self.assertEqual(thomas_messages[0].text, "Bonjour tout le monde !")

    def test_following_and_wall(self):
        """Epic 3 : Abonnements et agrégation sur le mur."""
        self.network.publish("Thomas", "Message de Thomas")
        self.network.publish("Alice", "Message d'Alice")
        self.network.publish("Bob", "Message de Bob") # Charlie ne suit pas Bob

        self.network.follow("Charlie", "Thomas")
        self.network.follow("Charlie", "Alice")

        charlie_wall = self.network.read_wall("Charlie")
        
        self.assertEqual(len(charlie_wall), 2)
        authors = [msg.author for msg in charlie_wall]
        self.assertIn("Thomas", authors)
        self.assertIn("Alice", authors)
        self.assertNotIn("Bob", authors)

    def test_mentions(self):
        """Epic 4 : Mentions d'utilisateurs."""
        self.network.publish("Alice", "Salut @Charlie, tu vas bien ?")
        self.network.publish("Bob", "J'adore ce réseau.")
        
        charlie_mentions = self.network.get_mentions("Charlie")
        
        self.assertEqual(len(charlie_mentions), 1)
        self.assertEqual(charlie_mentions[0].author, "Alice")

    def test_links(self):
        """Epic 5 : Partage de liens vers des messages."""
        msg = self.network.publish("Thomas", "Ceci est un message important.")
        link = msg.get_link()
        
        # Format attendu : https://social.net/msg/{id}
        self.assertTrue(link.startswith("https://social.net/msg/"))
        
        retrieved_msg = self.network.get_message_by_link(link)
        self.assertIsNotNone(retrieved_msg)
        self.assertEqual(retrieved_msg.text, "Ceci est un message important.")

    def test_direct_messages(self):
        """Epic 6 : Messages privés (Direct Messages)."""
        self.network.send_direct_message("Alice", "Thomas", "Salut Thomas, c'est secret !")
        self.network.publish("Alice", "Message public d'Alice") # Ne doit pas apparaître dans les DM
        
        thomas_dms = self.network.read_direct_messages("Thomas")
        self.assertEqual(len(thomas_dms), 1)
        self.assertEqual(thomas_dms[0].text, "Salut Thomas, c'est secret !")
        
        # Vérification qu'un autre utilisateur ne voit pas le DM
        charlie_dms = self.network.read_direct_messages("Charlie")
        self.assertEqual(len(charlie_dms), 0)
        
        # Vérification que le message privé n'apparaît pas sur les murs publics
        self.network.follow("Charlie", "Alice")
        charlie_wall = self.network.read_wall("Charlie")
        self.assertEqual(len(charlie_wall), 1)
        self.assertEqual(charlie_wall[0].text, "Message public d'Alice")


if __name__ == '__main__':
    unittest.main()