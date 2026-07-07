import unittest

from pygments.lexers import clean

"""
KATA : Code Cracker

Description du problème :
Étant donné une clé de déchiffrement de l'alphabet comme celle ci-dessous, 
créez un programme capable de déchiffrer n'importe quel message à l'aide de cette clé.

Alphabet :
    a b c d e f g h i j k l m n o p q r s t u v w x y z

Clé de déchiffrement :
    ! ) " ( £ * % & > < @ a b c d e f g h i j k l m n o

Vous devez également créer un programme de chiffrement qui chiffrera tout message 
que vous lui donnerez en utilisant cette même clé.

Consignes d'adaptation Python :
- Conserver les espaces ou les caractères inconnus s'il y en a.
- Gérer les minuscules (l'alphabet fourni étant en minuscules).
"""

alphabet: str = "abcdefghijklmnopqrstuvwxyz"
cle_dech: str = '!)"(£*%&><@abcdefghijklmno'


class CodeCracker:
    # Définition de l'alphabet de base et de la clé fournie dans l'énoncé

    def __init__(self):
        # Création des dictionnaires de correspondance (mapping) pour optimiser les performances
        # dict(zip(...)) associe chaque lettre à son symbole correspondant
        self.alph2cle = dict(zip(alphabet, cle_dech))
        self.cle2alph = dict(zip(cle_dech, alphabet))

    def encrypt(self, message: str) -> str:
        """
        Chiffre un message en remplaçant chaque lettre par le symbole de la clé.
        Les caractères non présents dans l'alphabet (comme les espaces) restent inchangés.
        """
        result = ""
        for m in message:
            m = m.lower()
            if m not in self.alph2cle:
                result += m
            else:
                result += self.alph2cle[m]
        return result

    def decrypt(self, encrypted_message: str) -> str:
        """
        Déchiffre un message en remplaçant chaque symbole par la lettre d'origine.
        Les caractères inconnus ou espaces restent inchangés.
        """
        result = ""
        for e in encrypted_message:
            if e not in self.cle2alph:
                result += e
            else:
                result += self.cle2alph[e]
        return result


class TestCodeCracker(unittest.TestCase):
    def setUp(self):
        """Initialisation de l'instance CodeCracker avant chaque test."""
        self.cracker = CodeCracker()

    def test_encrypt_single_letters(self):
        """Vérifie le chiffrement de lettres isolées."""
        self.assertEqual(self.cracker.encrypt("a"), "!")
        self.assertEqual(self.cracker.encrypt("b"), ")")
        self.assertEqual(self.cracker.encrypt("z"), "o")

    def test_decrypt_single_symbols(self):
        """Vérifie le déchiffrement de symboles isolés."""
        self.assertEqual(self.cracker.decrypt("!"), "a")
        self.assertEqual(self.cracker.decrypt(")"), "b")
        self.assertEqual(self.cracker.decrypt("o"), "z")

    def test_encrypt_full_word(self):
        """Vérifie le chiffrement d'un mot complet."""
        # hello -> h=&, e=£, l=b, o=e
        self.assertEqual(self.cracker.encrypt("hello"), "&£aad")

    def test_decrypt_full_word(self):
        """Vérifie le déchiffrement d'un mot complet."""
        self.assertEqual(self.cracker.decrypt("&£aad"), "hello")

    def test_handle_spaces_and_case(self):
        """Vérifie que les espaces sont préservés et que la casse est passée en minuscule."""
        # "hello world" -> h=&, e=£, l=b, o=e, w=l, r=g, d=(
        self.assertEqual(self.cracker.encrypt("Hello World"), "&£aad ldga(")
        self.assertEqual(self.cracker.decrypt("&£aad ldga("), "hello world")

    def test_round_trip(self):
        """Vérifie que le déchiffrement d'un message chiffré redonne bien le message d'origine."""
        original_message = "le code a ete cracke avec succes"
        encrypted = self.cracker.encrypt(original_message)
        decrypted = self.cracker.decrypt(encrypted)
        self.assertEqual(decrypted, original_message)


if __name__ == "__main__":
    # Exécution des tests unitaires
    unittest.main()
