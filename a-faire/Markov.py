import random
import unittest
from collections import defaultdict
from typing import Dict, List, Optional

# ==============================================================================
# CONSIGNES DU KATA (Traduites et adaptées en Français)
# ==============================================================================
"""
À propos de ce Kata :
Construire un générateur de texte basé sur une chaîne de Markov.

Objectif :
Créer un logiciel en deux parties pour générer du texte de manière 
pseudo-aléatoire à partir d'un texte d'apprentissage.

Partie 1 : Apprentissage (Extraction de statistiques)
  - Analyser un texte pour en extraire des statistiques.
  - Chaque mot doit avoir la liste des mots possibles qui le suivent.
  - Exemple avec le texte : "les hommes libres peuvent rester libres ou bien vendre leur liberté"
    L'analyse doit montrer que le mot "libres" peut être suivi de "peuvent" ou de "ou".
    (La fréquence est implicitement conservée si on stocke "peuvent" et "ou" dans une liste).

Partie 2 : Génération
  - Générer un texte à partir des statistiques précédentes.
  - La fonction prend en paramètre le nombre de mots du texte à générer.
  - Un paramètre optionnel permet de définir le premier mot du texte.
"""

# ==============================================================================
# VOTRE IMPLEMENTATION (Le Kata à résoudre)
# ==============================================================================

class MarkovChain:
    def __init__(self):
        # Utilisation d'un defaultdict pour stocker la liste des mots suivants
        self.stats: Dict[str, List[str]] = defaultdict(list)

    def train(self, text: str) -> None:
        """
        Partie 1: Analyse le texte et extrait les statistiques.
        Construit un dictionnaire où la clé est un mot, et la valeur est 
        une liste des mots qui le suivent (les doublons représentent les pourcentages).
        """
        if not text:
            return

        words = text.split()
        for i in range(len(words) - 1):
            current_word = words[i]
            next_word = words[i + 1]
            self.stats[current_word].append(next_word)

    def generate(self, length: int, start_word: Optional[str] = None) -> str:
        """
        Partie 2: Génère un texte de la longueur demandée à partir des statistiques.
        """
        if not self.stats or length <= 0:
            return ""

        # Si le mot de départ n'est pas fourni ou n'existe pas, on en prend un au hasard
        if start_word not in self.stats:
            start_word = random.choice(list(self.stats.keys()))

        generated_words = [start_word]
        current_word = start_word

        for _ in range(length - 1):
            next_words = self.stats.get(current_word)
            
            # Si le mot n'a pas de successeur (fin de phrase), on s'arrête prématurément
            if not next_words:
                break
                
            current_word = random.choice(next_words)
            generated_words.append(current_word)

        return " ".join(generated_words)


# ==============================================================================
# TESTS UNITAIRES (Validation du comportement)
# ==============================================================================

class TestMarkovChain(unittest.TestCase):

    def setUp(self):
        self.markov = MarkovChain()
        self.sample_text = "les hommes libres peuvent rester libres ou bien vendre leur liberté"

    def test_should_extract_correct_statistics(self):
        """Partie 1 : L'analyse doit lier les mots correctement."""
        self.markov.train(self.sample_text)
        
        # "les" est suivi de "hommes"
        self.assertEqual(self.markov.stats["les"], ["hommes"])
        
        # "libres" apparaît 2 fois, suivi de "peuvent" et "ou"
        self.assertEqual(self.markov.stats["libres"], ["peuvent", "ou"])
        
        # "liberté" est le dernier mot, il ne doit rien avoir comme successeur
        self.assertNotIn("liberté", self.markov.stats)

    def test_should_generate_text_of_exact_length(self):
        """Partie 2 : La génération doit respecter la longueur demandée."""
        self.markov.train(self.sample_text)
        
        # On force le point de départ pour éviter un blocage sur le dernier mot
        result = self.markov.generate(length=4, start_word="les")
        words_count = len(result.split())
        
        self.assertEqual(words_count, 4)

    def test_should_generate_coherent_chain(self):
        """Partie 2 : Les mots générés doivent logiquement se suivre selon le texte source."""
        # Fixer la seed permet de rendre le test déterministe
        random.seed(42)
        
        self.markov.train("chat mange souris chat dort souris court")
        # Les successeurs: 
        # chat -> mange, dort
        # mange -> souris
        # souris -> chat, court
        
        result = self.markov.generate(length=4, start_word="chat")
        
        # On vérifie que chaque mot est bien un successeur légitime du mot précédent
        words = result.split()
        for i in range(len(words) - 1):
            valid_next_words = self.markov.stats[words[i]]
            self.assertIn(words[i+1], valid_next_words)

    def test_should_stop_early_if_dead_end_reached(self):
        """Partie 2 : Si la chaîne tombe sur un mot sans successeur, elle doit s'arrêter."""
        self.markov.train("un deux trois")
        
        # Demander 10 mots en partant de "deux", on ne pourra avoir que "deux trois"
        result = self.markov.generate(length=10, start_word="deux")
        
        self.assertEqual(result, "deux trois")

if __name__ == '__main__':
    unittest.main()