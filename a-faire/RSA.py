import base64
import unittest

# =============================================================================
# KATA : CHIFFREMENT RSA
# =============================================================================
#
# CONSIGNES :
# L'algorithme RSA (Rivest–Shamir–Adleman) est un cryptosystème à clé publique 
# largement utilisé pour la transmission sécurisée de données.
# Dans ce kata, nous allons chiffrer et déchiffrer un message avec RSA.
#
# 1. Génération des clés (Théorie & Constantes fournies pour l'exercice) :
#    - Trouver 2 nombres premiers p et q tels que (2^24 + 1) < p * q < 2^32
#    - Calculer le module N = p * q
#    - Calculer l'indicatrice d'Euler n = (p - 1) * (q - 1)
#    - Choisir c, un nombre premier avec n tel que 1 < c < n. 
#      La clé publique est le couple (N, c).
#    - Déterminer d tel que d ≡ c^-1 (mod n) (inverse multiplicatif modulaire).
#      La clé privée est le couple (N, d).
#
# 2. Chiffrer le message :
#    - Prendre un message (chaîne de caractères) en entrée.
#    - Découper le message en blocs d'exactement 3 octets (bytes).
#    - Pour chaque bloc converti en entier 'a', calculer a^c (mod N).
#      Vous obtiendrez un entier sur 4 octets.
#    - La concaténation de tous ces nombres est le message chiffré (en bytes).
#
# 3. Déchiffrer le message :
#    - Prendre un message chiffré (bytes) en entrée.
#    - Découper ce message en blocs d'exactement 4 octets.
#    - Pour chaque bloc converti en entier 'a', calculer a^d (mod N).
#      Vous obtiendrez un entier sur 3 octets.
#    - La concaténation de tous ces nombres donne le message d'origine.
#
# 4. Transmettre le message :
#    - Créer une fonction d'encodage qui prend le message chiffré (bytes) et 
#      retourne une chaîne lisible en Base64.
#    - Créer la fonction inverse de décodage.
# =============================================================================

def encrypt_rsa(message: str, n_mod: int, c_pub: int) -> bytes:
    """Chiffre un message texte en utilisant la clé publique RSA (N, c)."""
    msg_bytes = message.encode('utf-8')
    
    # Ajout d'un padding (bourrage) si la taille n'est pas un multiple de 3
    padding_length = (3 - (len(msg_bytes) % 3)) % 3
    msg_bytes += b'\x00' * padding_length

    encrypted_data = bytearray()
    
    # Traitement par blocs de 3 octets
    for i in range(0, len(msg_bytes), 3):
        chunk = msg_bytes[i:i+3]
        # Convertit les 3 octets en un entier (Big Endian)
        a = int.from_bytes(chunk, byteorder='big')
        
        # Application de la formule RSA : a^c (mod N)
        enc_a = pow(a, c_pub, n_mod)
        
        # Le résultat chiffré est stocké sur 4 octets
        encrypted_data.extend(enc_a.to_bytes(4, byteorder='big'))
        
    return bytes(encrypted_data)


def decrypt_rsa(encrypted_bytes: bytes, n_mod: int, d_priv: int) -> str:
    """Déchiffre des données brutes en utilisant la clé privée RSA (N, d)."""
    decrypted_data = bytearray()
    
    # Traitement par blocs de 4 octets
    for i in range(0, len(encrypted_bytes), 4):
        chunk = encrypted_bytes[i:i+4]
        # Convertit les 4 octets en un entier
        a = int.from_bytes(chunk, byteorder='big')
        
        # Application de la formule RSA inverse : a^d (mod N)
        dec_a = pow(a, d_priv, n_mod)
        
        # Le résultat déchiffré est stocké sur 3 octets
        decrypted_data.extend(dec_a.to_bytes(3, byteorder='big'))
        
    # Suppression du padding potentiel et décodage en chaîne de caractères
    return decrypted_data.rstrip(b'\x00').decode('utf-8')


def encode_for_transmission(data: bytes) -> str:
    """Encode les données binaires en Base64 pour la transmission."""
    return base64.b64encode(data).decode('utf-8')


def decode_from_transmission(data: str) -> bytes:
    """Décode la chaîne Base64 reçue en données binaires."""
    return base64.b64decode(data)


# =============================================================================
# TESTS UNITAIRES
# =============================================================================

class TestRSAKata(unittest.TestCase):
    
    def setUp(self):
        # Paramètres d'exemple fournis par le Kata
        self.p = 51581
        self.q = 60101
        self.N = 3100069681
        self.c = 66797
        self.d = 1336940133
        self.message = "Hello world!"
        self.expected_base64 = "FQGtKYcinGkgGvkOQ2pvWw=="
        
        # Valeurs chiffrées attendues en décimal pour chaque bloc de 3 octets
        self.expected_decimal_chunks = [352431401, 2267192425, 538638606, 1131048795]

    def test_encryption_chunks(self):
        """Vérifie que les calculs intermédiaires de chiffrement sont corrects."""
        encrypted_bytes = encrypt_rsa(self.message, self.N, self.c)
        
        # Vérifie la taille de la sortie (4 blocs de 4 octets = 16 octets)
        self.assertEqual(len(encrypted_bytes), 16)
        
        # Vérifie les entiers générés
        actual_chunks = []
        for i in range(0, len(encrypted_bytes), 4):
            chunk = encrypted_bytes[i:i+4]
            actual_chunks.append(int.from_bytes(chunk, byteorder='big'))
            
        self.assertEqual(actual_chunks, self.expected_decimal_chunks)

    def test_base64_transmission(self):
        """Vérifie l'encodage de transmission en Base64."""
        encrypted_bytes = encrypt_rsa(self.message, self.N, self.c)
        encoded_message = encode_for_transmission(encrypted_bytes)
        
        self.assertEqual(encoded_message, self.expected_base64)

    def test_full_round_trip(self):
        """Vérifie le cycle complet : Chiffrement -> Encodage -> Décodage -> Déchiffrement."""
        # Emetteur
        encrypted_bytes = encrypt_rsa(self.message, self.N, self.c)
        transmitted_string = encode_for_transmission(encrypted_bytes)
        
        # Récepteur
        received_bytes = decode_from_transmission(transmitted_string)
        decrypted_message = decrypt_rsa(received_bytes, self.N, self.d)
        
        self.assertEqual(decrypted_message, self.message)

if __name__ == '__main__':
    unittest.main()