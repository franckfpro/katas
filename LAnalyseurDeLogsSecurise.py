"""
KATA PYTHON #046 - L'Analyseur de Logs Sécurisé
Difficulté : 3/10

ÉNONCÉ :
Vous écrivez un script pour analyser les fichiers de logs d'un serveur. Chaque
ligne du fichier représente une requête et suit un format strict :
"DATE | CODE_STATUT | MESSAGE" (ex: "2026-06-18 | 200 | OK")

On vous demande de compléter la fonction `analyser_logs`. Elle prend en paramètre
un flux de texte (simulant un fichier ouvert) et doit renvoyer un dictionnaire
contenant le compte de chaque code statut rencontré.

RÈGLES ET CONTRAINTES :
1. Vous devez lire le flux ligne par ligne.
2. Si une ligne est valide, vous devez extraire le `CODE_STATUT` (qui doit être
   converti en entier `int`) et incrémenter son compteur dans le dictionnaire.
3. Sécurité (Gestion des erreurs) : Si une ligne est mal formatée, s'il manque des
   séparateurs "|", ou si le code statut n'est pas un nombre valide, la fonction
   ne doit PAS planter. Elle doit simplement ignorer cette ligne et passer à la suivante.
4. Les espaces superflus autour des éléments (ex: " 200 ") doivent être nettoyés.

Exemple de contenu :
2026-06-18 | 200 | OK
2026-06-18 | 404 | Not Found
LIGNE_CORROMPUE_SANS_SEPARATEUR
2026-06-18 | 200 | Success

Résultat attendu : {200: 2, 404: 1}
"""

import io
import unittest


def analyser_logs(flux_fichier: io.TextIOBase) -> dict[int, int]:
    """Analyse un flux de logs et compte les occurrences de chaque code statut int.

    Ignore les lignes corrompues ou mal formées.
    """
    # TODO: Implémenter la logique ici
    pass


# =====================================================================
# TESTS UNITAIRES (Ne pas modifier cette section)
# =====================================================================


class TestAnalyseurLogs(unittest.TestCase):
    """Suite de tests pour valider votre fonction analyser_logs."""

    def test_analyse_standard(self):
        """Cas nominal avec un fichier de logs bien formé."""
        contenu = (
            "2026-06-18 | 200 | OK\n"
            "2026-06-18 | 404 | Not Found\n"
            "2026-06-18 | 200 | Re-OK\n"
            "2026-06-18 | 500 | Internal Error\n"
        )
        # io.StringIO simule un fichier ouvert en mémoire à partir d'une string
        fichier_virtuel = io.StringIO(contenu)

        attendu = {200: 2, 404: 1, 500: 1}
        self.assertEqual(analyser_logs(fichier_virtuel), attendu)

    def test_gestion_erreurs_format(self):
        """Le script ne doit pas crasher si le format ou le type est incorrect."""
        contenu = (
            "2026-06-18 | 200 | OK\n"
            "Ligne corrompue sans pipe\n"
            "2026-06-18 | PAS_UN_NOMBRE | Erreur de type\n"
            "2026-06-18 | 404 | Toujours vivant\n"
        )
        fichier_virtuel = io.StringIO(contenu)

        attendu = {200: 1, 404: 1}
        self.assertEqual(analyser_logs(fichier_virtuel), attendu)

    def test_nettoyage_espaces(self):
        """Les espaces autour du code statut ne doivent pas gêner la conversion."""
        contenu = (
            "2026-06-18 |   200   | OK avec espaces\n" "2026-06-18 | 200| OK collé\n"
        )
        fichier_virtuel = io.StringIO(contenu)

        attendu = {200: 2}
        self.assertEqual(analyser_logs(fichier_virtuel), attendu)


if __name__ == "__main__":
    unittest.main(verbosity=2)
