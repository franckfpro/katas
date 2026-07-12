import unittest

"""
KATA BANK OCR

Objectif :
Développer un parseur et validateur de numéros de compte bancaire 
lus par une machine de reconnaissance optique de caractères (OCR).

Règles de validation (Checksum) :
Pour le numéro "345882865" :
d9 d8 d7 d6 d5 d4 d3 d2 d1
 3  4  5  8  8  2  8  6  5

        _  _     _  _  _  _  _ 
      | _| _||_||_ |_   ||_||_|
      ||_  _|  | _||_|  ||_| _|
                               

Formule : (1*d1 + 2*d2 + 3*d3 + ... + 9*d9) mod 11 == 0
"""

class AnalyseurOCR:
    # Dictionnaire de correspondance entre les caractères 3x3 et le chiffre réel
    # Chaque chaîne fait exactement 9 caractères (3 lignes concaténées).
    DIGITS_MAP = {
        " _ | ||_|": "0",
        "     |  |": "1",
        " _  _||_ ": "2",
        " _  _| _|": "3",
        "   |_|  |": "4",
        " _ |_  _|": "5",
        " _ |_ |_|": "6",
        " _   |  |": "7",
        " _ |_||_|": "8",
        " _ |_| _|": "9"
    }

    @classmethod
    def parser_entree(cls, entree: str) -> str:
        """
        User Story 1 : 
        Transforme une chaîne OCR de 3 lignes x 27 colonnes en un compte de 9 chiffres.
        """
        lignes = entree.split('\n')
        
        # Sécurité : on s'assure d'avoir au moins les 3 lignes requises
        if len(lignes) < 3:
            return "?" * 9
            
        compte = ""
        # On découpe l'entrée tous les 3 caractères pour lire chiffre par chiffre
        for i in range(0, 27, 3):
            # Concaténation des 3 lignes pour un même bloc vertical
            bloc_3x3 = lignes[0][i:i+3] + lignes[1][i:i+3] + lignes[2][i:i+3]
            compte += cls.DIGITS_MAP.get(bloc_3x3, "?")
            
        return compte

    @staticmethod
    def est_valide(compte: str) -> bool:
        """
        User Story 2 : 
        Vérifie la validité du compte via la formule du checksum.
        """
        # Un compte illisible ou incomplet n'est pas valide
        if "?" in compte or len(compte) != 9:
            return False
            
        # reversed(compte) permet de traiter le chiffre le plus à droite avec l'index 0
        somme = sum(int(chiffre) * (index + 1) for index, chiffre in enumerate(reversed(compte)))
        return somme % 11 == 0

    @classmethod
    def evaluer_compte(cls, entree: str) -> str:
        """
        User Story 3 : 
        Formate la sortie finale en ajoutant les mentions ILL (Illisible) 
        ou ERR (Erreur de validation) si nécessaire.
        """
        compte = cls.parser_entree(entree)
        
        if "?" in compte:
            return f"{compte} ILL"
        elif not cls.est_valide(compte):
            return f"{compte} ERR"
        else:
            return compte


# --- TESTS UNITAIRES ---

class TestAnalyseurOCR(unittest.TestCase):
    
    def test_us1_parser_des_zeros(self):
        """Vérifie la bonne lecture d'une ligne de zéros."""
        entree_ocr = (
            " _  _  _  _  _  _  _  _  _ \n"
            "| || || || || || || || || |\n"
            "|_||_||_||_||_||_||_||_||_|\n"
        )
        self.assertEqual(AnalyseurOCR.parser_entree(entree_ocr), "000000000")

    def test_us1_parser_les_chiffres_1_a_9(self):
        """Vérifie la bonne lecture de tous les chiffres de 1 à 9."""
        entree_ocr = (
            "    _  _     _  _  _  _  _ \n"
            "  | _| _||_||_ |_   ||_||_|\n"
            "  ||_  _|  | _||_|  ||_| _|\n"
        )
        self.assertEqual(AnalyseurOCR.parser_entree(entree_ocr), "123456789")

    def test_us2_checksum_valide(self):
        """
        Vérifie qu'un compte valide passe avec succès le contrôle (mod 11).
        (123456789 donne 165, qui est un multiple de 11).
        """
        self.assertTrue(AnalyseurOCR.est_valide("123456789"))
        self.assertTrue(AnalyseurOCR.est_valide("000000000"))

    def test_us2_checksum_invalide(self):
        """Vérifie le rejet d'un compte ne passant pas le contrôle."""
        self.assertFalse(AnalyseurOCR.est_valide("111111111"))

    def test_us3_evaluation_compte_valide(self):
        """Un compte valide n'a pas de suffixe d'erreur."""
        entree_ocr = (
            "    _  _     _  _  _  _  _ \n"
            "  | _| _||_||_ |_   ||_||_|\n"
            "  ||_  _|  | _||_|  ||_| _|\n"
        )
        self.assertEqual(AnalyseurOCR.evaluer_compte(entree_ocr), "123456789")

    def test_us3_evaluation_compte_en_erreur(self):
        """Un compte sans '?' mais avec un mauvais checksum se voit affublé de 'ERR'."""
        entree_ocr = (
            "                           \n"
            "  |  |  |  |  |  |  |  |  |\n"
            "  |  |  |  |  |  |  |  |  |\n"
        )
        self.assertEqual(AnalyseurOCR.evaluer_compte(entree_ocr), "111111111 ERR")

    def test_us3_evaluation_compte_illisible(self):
        """Un compte contenant des caractères mal formés se voit affublé de 'ILL'."""
        entree_ocr_corrompu = (
            "    _  _     _  _  _  _  _ \n"
            "  | _| _||_||_ |_   ||_||_|\n"
            "  ||_  _|  | _||_|  | _  _|\n"  # La ligne du '8' (avant-dernier chiffre) a été modifiée
        )
        self.assertEqual(AnalyseurOCR.evaluer_compte(entree_ocr_corrompu), "1234567?9 ILL")


if __name__ == '__main__':
    unittest.main()
