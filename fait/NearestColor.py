"""
KATA : Couleur la plus proche (Nearest Color)

INTRODUCTION :
Une couleur est composée d'une quantité de rouge, vert et bleu (RVB).
En informatique, chaque quantité est comprise entre 0 et 255 (en décimal),
soit de 00 à FF en hexadécimal.
Pour cet exercice, nous utiliserons une notation simplifiée à 3 caractères (de 0 à F) :
- 'F00' pour le rouge
- '0F0' pour le vert
- '00F' pour le bleu

PARTIE 1 : La couleur la plus proche
L'idée est d'utiliser un ensemble de couleurs de base (ex: ['F00', '0F0', '00F'])
et de trouver la couleur la plus proche de la couleur cible parmi cet ensemble.
Exemple : La couleur la plus proche de 'F42' est 'F00'.

PARTIE 2 : En cas d'égalité
Il faut lister toutes les couleurs en cas d'égalité.
Exemple : Le jaune 'FF0' est à égale distance du rouge 'F00' et du vert '0F0'.
La fonction doit donc retourner ces deux couleurs.
"""

import unittest


def get_nearest_colors(target_color: str, palette: list[str]) -> list[str]:
    """
    Très mauvaise solution mais on refera le kata

    """
    result: list[str] = []
    convertHex: dict(str, int) = {"A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15}

    targetColorConvert: list[int] = []
    for s in target_color:
        if s in convertHex:
            targetColorConvert.append(convertHex[s])
        else:
            targetColorConvert.append(int(s))

    paletteConvert: list[list[int]] = []
    for p in palette:
        plist: list[int] = []
        for s in p:
            if s in convertHex:
                plist.append(convertHex[s])
            else:
                plist.append(int(s))
        paletteConvert.append(plist)

    totallist: list[int] = []
    for pal in paletteConvert:
        for pos in range(3):
            pal[pos] -= targetColorConvert[pos]

        total = sum(abs(p) for p in pal)
        totallist.append(total)
    totallistmin = min(totallist)

    indexlist: list[int] = []
    for i, t in enumerate(totallist):
        if t == totallistmin:
            indexlist.append(i)

    for i in indexlist:
        result.append(palette[i])
    return result


"""
Autre solution:
def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    r = int(hex_color[0], 16)
    g = int(hex_color[1], 16)
    b = int(hex_color[2], 16)
    return r, g, b

def get_nearest_colors(target_color: str, palette: list[str]) -> list[str]:
  
    if not palette:
        return []

    target_rgb = hex_to_rgb(target_color)
    
    # Dictionnaire pour stocker la distance de chaque couleur de la palette
    distances = {}
    
    for color in palette:
        r, g, b = hex_to_rgb(color)
        # Formule de la distance euclidienne : sqrt((r1-r2)^2 + (g1-g2)^2 + (b1-b2)^2)
        distance = math.sqrt(
            (target_rgb[0] - r) ** 2 + 
            (target_rgb[1] - g) ** 2 + 
            (target_rgb[2] - b) ** 2
        )
        distances[color] = distance

    # Trouver la distance minimale
    min_distance = min(distances.values())
    
    # Récupérer toutes les couleurs qui partagent cette distance minimale (gestion des égalités)
    return [color for color, dist in distances.items() if dist == min_distance]


"""


# ==============================================================================
# TESTS UNITAIRES
# ==============================================================================


class TestNearestColor(unittest.TestCase):

    def setUp(self):
        # Palette de base demandée par l'énoncé
        self.palette = ["F00", "0F0", "00F"]

    def test_exact_match(self):
        """Doit retourner la couleur exacte si elle est présente dans la palette."""
        self.assertEqual(get_nearest_colors("F00", self.palette), ["F00"])

    def test_part_1_nearest_color(self):
        """Test de la partie 1 : 'F42' doit être plus proche de 'F00'."""
        self.assertEqual(get_nearest_colors("F42", self.palette), ["F00"])

    def test_part_2_equality(self):
        """Test de la partie 2 : 'FF0' (jaune) doit retourner 'F00' (rouge) et '0F0' (vert)."""
        result = get_nearest_colors("FF0", self.palette)
        # L'ordre dans la liste de retour dépend de l'ordre de la palette originale
        self.assertCountEqual(result, ["F00", "0F0"])

    def test_grey_equality(self):
        """Le gris '888' doit être à égale distance des trois couleurs primaires."""
        result = get_nearest_colors("888", self.palette)
        self.assertCountEqual(result, ["F00", "0F0", "00F"])


if __name__ == "__main__":
    print(get_nearest_colors("F00", ["F00", "0F0", "00F"]))
    # unittest.main()
