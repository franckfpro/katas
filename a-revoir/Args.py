import unittest
from typing import Any, Dict, List, Type

# =============================================================================
# KATA : Args (Parseur d'arguments de ligne de commande)
# =============================================================================
#
# CONSIGNES :
#
# La plupart d'entre nous ont déjà eu à analyser des arguments de ligne de
# commande. Écrivons notre propre utilitaire !
#
# Les arguments passés au programme sont constitués de "flags" (drapeaux)
# et de valeurs. Les flags doivent être constitués d'un seul caractère,
# précédé d'un signe moins (-). Chaque flag peut être associé à zéro ou
# une valeur.
#
# Vous devez écrire un parseur qui prend un "schéma" détaillant les
# arguments attendus (nombre et types). Une fois le schéma spécifié, le
# programme passe la liste réelle des arguments au parseur. Celui-ci
# vérifie que les arguments correspondent au schéma.
#
# Exemple d'appel : -l -p 8080 -d /usr/logs
# Schéma correspondant : 3 flags (l, p, d).
# - "l" (logging) : flag booléen, True si présent, False sinon (aucune valeur).
# - "p" (port) : entier.
# - "d" (directory) : chaîne de caractères.
#
# Valeurs par défaut si le flag est absent :
# - Booléen : False
# - Entier : 0
# - Chaîne : ""
#
# Erreurs : Si les arguments ne correspondent pas au schéma, un message
# d'erreur clair et précis doit être levé.
#
# Extensibilité : Votre code doit rendre évidente et simple l'intégration
# de nouveaux types de valeurs.
#
# Bonus (Ambitieux) :
# Supporter les listes (ex: -g this,is,a,list -d 1,2,-3,5).
# =============================================================================

class ArgsException(Exception):
    """Exception personnalisée pour gérer les erreurs de parsing."""
    pass

class ArgsParser:
    def __init__(self, schema: Dict[str, Type]):
        """
        Initialise le parseur avec un schéma définissant les flags et leurs types.
        Exemple : {'l': bool, 'p': int, 'd': str}
        """
        self.schema = schema
        self.parsed_values: Dict[str, Any] = {}
        self._initialize_defaults()

    def _initialize_defaults(self) -> None:
        """Initialise les valeurs par défaut pour chaque flag selon son type."""
        for flag, flag_type in self.schema.items():
            if flag_type == bool:
                self.parsed_values[flag] = False
            elif flag_type == int:
                self.parsed_values[flag] = 0
            elif flag_type == str:
                self.parsed_values[flag] = ""
            elif flag_type == list:
                self.parsed_values[flag] = []
            else:
                raise ArgsException(f"Type non supporté pour le flag '{flag}': {flag_type}")

    def parse(self, args_list: List[str]) -> None:
        """
        Analyse la liste des arguments fournis et peuple les valeurs internes.
        Lève une ArgsException en cas d'argument invalide ou non conforme au schéma.
        """
        i = 0
        while i < len(args_list):
            arg = args_list[i]
            if not arg.startswith('-'):
                raise ArgsException(f"Argument invalide : '{arg}'. Les arguments doivent commencer par '-'.")

            flag = arg[1:]
            if flag not in self.schema:
                raise ArgsException(f"Flag inattendu : '{flag}'.")

            flag_type = self.schema[flag]

            if flag_type == bool:
                self.parsed_values[flag] = True
                i += 1
            else:
                if i + 1 >= len(args_list):
                    raise ArgsException(f"Valeur manquante pour le flag '{flag}'.")
                next_arg = args_list[i + 1]
                #if next_arg.startswith('-'):
                #    raise ArgsException(f"Valeur manquante pour le flag '{flag}'.")

                try:
                    if flag_type == int:
                        self.parsed_values[flag] = int(next_arg)
                    elif flag_type == str:
                        self.parsed_values[flag] = next_arg
                    elif flag_type == list:
                        self.parsed_values[flag] = next_arg.split(',')
                    else:
                        raise ArgsException(f"Type non supporté pour le flag '{flag}': {flag_type}")
                except ValueError as e:
                    raise ArgsException(f"Valeur invalide pour le flag {e} '{flag}': '{next_arg}'.")

                i += 2

    def get_boolean(self, flag: str) -> bool:
        """Retourne la valeur booléenne associée au flag."""
        if flag not in self.schema:
            raise ArgsException(f"Flag inconnu : '{flag}'.")
        return self.parsed_values.get(flag, False)

    def get_integer(self, flag: str) -> int:
        """Retourne la valeur entière associée au flag."""
        if flag not in self.schema:
            raise ArgsException(f"Flag inconnu : '{flag}'.")
        return self.parsed_values.get(flag, 0)

    def get_string(self, flag: str) -> str:
        """Retourne la chaîne de caractères associée au flag."""
        if flag not in self.schema:
            raise ArgsException(f"Flag inconnu : '{flag}'.")
        return self.parsed_values.get(flag, "")

    def get_list(self, flag: str) -> List[str]:
        """Retourne la liste associée au flag (bonus)."""
        if flag not in self.schema:
            raise ArgsException(f"Flag inconnu : '{flag}'.")
        return self.parsed_values.get(flag, [])

# =============================================================================
# TESTS UNITAIRES
# =============================================================================

class TestArgsParser(unittest.TestCase):

    def test_simple_boolean_present(self):
        parser = ArgsParser({'l': bool})
        parser.parse(["-l"])
        self.assertTrue(parser.get_boolean('l'))

    def test_simple_boolean_missing(self):
        parser = ArgsParser({'l': bool})
        parser.parse([])
        self.assertFalse(parser.get_boolean('l'))

    def test_integer_and_string(self):
        parser = ArgsParser({'p': int, 'd': str})
        parser.parse(["-p", "8080", "-d", "/usr/logs"])
        self.assertEqual(parser.get_integer('p'), 8080)
        self.assertEqual(parser.get_string('d'), "/usr/logs")

    def test_order_does_not_matter(self):
        parser = ArgsParser({'l': bool, 'p': int, 'd': str})
        parser.parse(["-d", "/usr/logs", "-l", "-p", "8080"])
        self.assertTrue(parser.get_boolean('l'))
        self.assertEqual(parser.get_integer('p'), 8080)
        self.assertEqual(parser.get_string('d'), "/usr/logs")

    def test_negative_integer_parsing_is_not_confused_with_flag(self):
        parser = ArgsParser({'p': int})
        parser.parse(["-p", "-42"])
        self.assertEqual(parser.get_integer('p'), -42)

    def test_default_values_are_assigned_when_flags_missing(self):
        parser = ArgsParser({'l': bool, 'p': int, 'd': str})
        parser.parse([])
        self.assertFalse(parser.get_boolean('l'))
        self.assertEqual(parser.get_integer('p'), 0)
        self.assertEqual(parser.get_string('d'), "")

    def test_raises_exception_on_invalid_argument_type(self):
        parser = ArgsParser({'p': int})
        with self.assertRaises(ArgsException):
            parser.parse(["-p", "not_an_integer"])

    def test_raises_exception_on_unexpected_flag(self):
        parser = ArgsParser({'l': bool})
        with self.assertRaises(ArgsException):
            parser.parse(["-x"])

    def test_ambitious_list_parsing(self):
        parser = ArgsParser({'g': list, 'd': list})
        parser.parse(["-g", "this,is,a,list", "-d", "1,2,-3,5"])
        self.assertEqual(parser.get_list('g'), ["this", "is", "a", "list"])
        self.assertEqual(parser.get_list('d'), ["1", "2", "-3", "5"])

if __name__ == '__main__':
    unittest.main(verbosity=2)