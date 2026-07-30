import itertools
from collections import Counter
import unittest

# =============================================================================
# KATA : TEXAS HOLD'EM
# =============================================================================
#
# CONSIGNES :
# Vous travaillez pour une chaîne de télévision diffusant un tournoi de 
# Texas Hold'Em. Les présentateurs ont besoin d'un programme rapide pour 
# afficher les mains des joueurs et désigner le gagnant à la fin d'une manche.
#
# En entrée, chaque joueur (et ses cartes) est représenté sur une ligne.
# - Une carte est composée de 2 caractères : la valeur (2-9, T, J, Q, K, A) 
#   et la couleur (c=clubs/trèfles, d=diamonds/carreaux, h=hearts/cœurs, s=spades/piques).
# - Un joueur qui ne se couche pas a 7 cartes (2 en main + 5 communes).
# - Un joueur qui se couche n'a que ses cartes en main et les cartes communes 
#   dévoilées avant qu'il ne se couche (le code ci-dessous se concentre sur 
#   l'évaluation des mains complètes).
#
# En sortie, le programme doit afficher pour chaque joueur :
# 1. Les cartes réorganisées : d'abord les cartes constituant la combinaison,
#    puis les kickers (cartes d'appui), puis les 2 cartes non utilisées.
# 2. Le nom de la combinaison (ex: "Flush", "Two Pairs").
# 3. La mention "(winner)" pour le(s) gagnant(s) de la manche.
#
# REGLES DU POKER (Ordre décroissant) :
# 8: Straight Flush, 7: Four of a kind, 6: Full House, 5: Flush, 
# 4: Straight, 3: Three of a kind, 2: Two Pairs, 1: Pair, 0: High Card.
# =============================================================================

# Dictionnaire pour convertir la valeur de la carte en entier
VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
          'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
RANK_NAMES = ["High Card", "Pair", "Two Pairs", "Three of a Kind", 
              "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush"]

class Card:
    def __init__(self, raw_str):
        self.raw = raw_str
        self.value = VALUES[raw_str[0]]
        self.suit = raw_str[1]

    def __repr__(self):
        return self.raw

    # Rendre les cartes triables par valeur décroissante
    def __lt__(self, other):
        return self.value > other.value

def evaluate_5_card_hand(cards):
    """
    Évalue une main exacte de 5 cartes.
    Retourne un tuple : (Score_Combinaison, [valeurs pour départager], [Cartes de la combi/kickers])
    """
    cards = sorted(cards) # Tri décroissant
    values = [c.value for c in cards]
    suits = [c.suit for c in cards]
    
    counts = Counter(values)
    freqs = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)
    
    is_flush = len(set(suits)) == 1
    
    # Gestion de la quinte (Straight) et du cas spécial de l'As (A, 2, 3, 4, 5)
    is_straight = False
    if len(counts) == 5 and values[0] - values[4] == 4:
        is_straight = True
    elif values == [14, 5, 4, 3, 2]: # Quinte blanche (As vaut 1)
        is_straight = True
        values = [5, 4, 3, 2, 14] # On déplace l'As à la fin pour le tri
        
    # Analyse des fréquences pour déterminer la combinaison
    if is_straight and is_flush:
        rank = 8
    elif freqs[0][1] == 4:
        rank = 7
    elif freqs[0][1] == 3 and freqs[1][1] == 2:
        rank = 6
    elif is_flush:
        rank = 5
    elif is_straight:
        rank = 4
    elif freqs[0][1] == 3:
        rank = 3
    elif freqs[0][1] == 2 and freqs[1][1] == 2:
        rank = 2
    elif freqs[0][1] == 2:
        rank = 1
    else:
        rank = 0

    # L'ordre de tri pour les départages : basé sur la fréquence puis la valeur
    tie_breaker = [item[0] for item in freqs]
    
    # On réorganise physiquement les cartes pour l'affichage (combi d'abord, puis kickers)
    sorted_cards_by_role = []
    for val in tie_breaker:
        sorted_cards_by_role.extend([c for c in cards if c.value == val])

    return (rank, tie_breaker, sorted_cards_by_role)

def find_best_hand(seven_cards):
    """
    Trouve la meilleure main de 5 cartes parmi 7.
    """
    best_eval = None
    best_unused = None
    
    for combo in itertools.combinations(seven_cards, 5):
        current_eval = evaluate_5_card_hand(combo)
        if best_eval is None or current_eval > best_eval:
            best_eval = current_eval
            # Les cartes non utilisées sont celles qui ne sont pas dans le combo
            best_unused = [c for c in seven_cards if c not in combo]
            
    # Tri des cartes non utilisées (décroissant)
    best_unused.sort()
    return best_eval, best_unused

def process_game(players_input):
    """
    Reçoit une liste de chaînes (une par joueur) contenant leurs 7 cartes.
    Détermine le(s) gagnant(s) et formate la sortie.
    """
    players_data = []
    best_score = None
    
    for line in players_input:
        raw_cards = line.strip().split()
        cards = [Card(c) for c in raw_cards]
        
        # On assume pour simplifier que le joueur n'a pas foldé (7 cartes présentes)
        if len(cards) == 7:
            evaluation, unused = find_best_hand(cards)
            players_data.append({
                'raw': line,
                'eval': evaluation,
                'unused': unused,
                'rank_name': RANK_NAMES[evaluation[0]],
                'score': (evaluation[0], evaluation[1])
            })
            
            if best_score is None or players_data[-1]['score'] > best_score:
                best_score = players_data[-1]['score']

    # Formatage de la sortie
    output = []
    for p in players_data:
        # Reconstruire l'ordre des cartes: 5 utilisées + 2 non utilisées
        ordered_cards = p['eval'][2] + p['unused']
        cards_str = " ".join([c.raw for c in ordered_cards])
        
        is_winner = " (winner)" if p['score'] == best_score else ""
        output.append(f"{cards_str} {p['rank_name']}{is_winner}")
        
    return output


# =============================================================================
# TESTS UNITAIRES
# =============================================================================

class TestTexasHoldEm(unittest.TestCase):

    def test_evaluate_high_card(self):
        cards = [Card(c) for c in ["2h", "4d", "6s", "8c", "Th"]]
        eval_result = evaluate_5_card_hand(cards)
        self.assertEqual(eval_result[0], 0) # High Card

    def test_evaluate_flush(self):
        cards = [Card(c) for c in ["2h", "4h", "6h", "8h", "Th"]]
        eval_result = evaluate_5_card_hand(cards)
        self.assertEqual(eval_result[0], 5) # Flush

    def test_find_best_hand_out_of_7(self):
        # Un joueur a une paire de 9 en main, et le board affiche une paire de Dames et un 3.
        # Il devrait obtenir "Two Pairs" (Q et 9) avec un kicker As.
        seven_cards = [Card(c) for c in ["9h", "9d", "Qc", "Qs", "Ac", "3d", "2h"]]
        best_eval, unused = find_best_hand(seven_cards)
        
        self.assertEqual(best_eval[0], 2) # Two Pairs
        # Les valeurs pour départager: Dames(12), Neufs(9), As(14)
        self.assertEqual(best_eval[1], [12, 9, 14]) 
        # Les cartes non utilisées doivent être le 3 et le 2
        self.assertEqual([c.raw for c in unused], ["3d", "2h"])

    def test_full_game_scenario(self):
        # Scénario avec 3 joueurs
        # Joueur 1 : Brelan de Dames (Three of a Kind)
        # Joueur 2 : Couleur à Pique (Flush) -> Gagnant
        # Joueur 3 : Deux paires (Two Pairs)
        inputs = [
            "Qh Qd 2c 3s 4d Qc 9h", # P1: Qh, Qd, Qc (Brelan de Dames)
            "As Ks 2s 5s Jc 9s 2h", # P2: As, Ks, 9s, 5s, 2s (Flush Piques)
            "Jh Jd 2c 3s 4d 2h 9c"  # P3: Jh, Jd, 2c, 2h (Deux paires Valets et 2)
        ]
        
        results = process_game(inputs)
        
        self.assertTrue("Three of a Kind" in results[0])
        self.assertFalse("(winner)" in results[0])
        
        self.assertTrue("Flush" in results[1])
        self.assertTrue("(winner)" in results[1])
        
        self.assertTrue("Two Pairs" in results[2])
        self.assertFalse("(winner)" in results[2])

if __name__ == '__main__':
    unittest.main()