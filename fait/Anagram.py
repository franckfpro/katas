import unittest

# =============================================================================
# KATA : Anagrammes de deux mots (Self-documenting code)
# =============================================================================
#
# CONSIGNES :
#
# Étape 1 :
# Écrivez un programme qui génère toutes les anagrammes composées de
# deux mots pour une chaîne de caractères donnée (ex: "documenting").
#
# Contrainte principale : Vous devez vous concentrer sur la LISIBILITÉ
# de votre code. Vous ne devez inclure aucun commentaire explicatif dans
# votre logique métier. Le but est de créer un code que n'importe qui
# peut lire et comprendre facilement (respect des standards PEP 8,
# nommage explicite, typage).
#
# Étape 2 :
# Essayez d'améliorer les performances de votre solution, mais gardez
# à l'esprit que l'optimisation affecte souvent la lisibilité.
# Continuez de privilégier la LISIBILITÉ avant tout.
#
# =============================================================================


def find_two_word_anagrams(target: str, valid_words: list[str]) -> set[tuple[str, str]]:
    """
    Retourne un ensemble de paires de mots (tuples) provenant de `valid_words`
    qui, combinées, forment une anagramme exacte de `target`.
    """
    toutes_possibilites = []
    result = set()
    for i in range(len(valid_words)):
        for j in range(len(valid_words)):
            if i != j:
                toutes_possibilites.append([valid_words[i], valid_words[j]])

    for paires in toutes_possibilites:
        if sorted(target) == sorted("".join(paires[0]) + "".join(paires[1])):
            result.add(tuple(paires))
    return result


# =============================================================================
# TESTS UNITAIRES
# =============================================================================


class TestTwoWordAnagrams(unittest.TestCase):

    def setUp(self):
        # Un dictionnaire réduit pour tester la logique unitaire
        self.dictionary = [
            "a",
            "c",
            "cat",
            "act",
            "o",
            "to",
            "cot",
            "at",
            "taco",
            "doc",
            "men",
            "ting",
        ]

    def test_finds_valid_two_word_anagrams(self):
        target = "cato"
        # "cat" + "o" = c, a, t, o
        # "act" + "o" = a, c, t, o
        # "cot" + "a" = c, o, t, a
        expected = {
            ("cat", "o"),
            ("o", "cat"),
            ("act", "o"),
            ("o", "act"),
            ("cot", "a"),
            ("a", "cot"),
        }

        result = find_two_word_anagrams(target, self.dictionary)
        self.assertEqual(result, expected)

    def test_no_anagram_possible(self):
        target = "python"
        expected = set()

        result = find_two_word_anagrams(target, self.dictionary)
        self.assertEqual(result, expected)

    def test_target_with_exact_dictionary_match(self):
        target = "ting"
        # "ting" est un seul mot, le kata demande DEUX mots.
        expected = set()

        result = find_two_word_anagrams(target, self.dictionary)
        self.assertEqual(result, expected)

    def test_complex_anagram(self):
        target = "documenting"
        # Simulation avec un dictionnaire partiel pour vérifier si l'algorithme
        # gère des mots plus longs. (Dans la réalité, il faudrait charger word_list.txt)
        custom_dict = ["document", "ing", "doc", "umenting", "do", "cumenting"]
        expected = {
            ("document", "ing"),
            ("ing", "document"),
            ("doc", "umenting"),
            ("umenting", "doc"),
            ("do", "cumenting"),
            ("cumenting", "do"),
        }

        result = find_two_word_anagrams(target, custom_dict)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
