import unittest

# ==============================================================================
# KATA : RPG COMBAT
# ==============================================================================
#
# CONSIGNES :
# Ce kata consiste à construire des règles de combat simples pour un jeu de rôle 
# (RPG). Il s'implémente comme une séquence d'itérations. Le domaine n'inclut 
# pas de carte complexe, mais nécessite la gestion de portées d'attaque.
#
# -- Itération 1 --
# 1. Tous les personnages, à leur création, ont : 
#    - Santé (Health) à 1000, Niveau (Level) à 1, et sont Vivants (Alive).
# 2. Les personnages peuvent infliger des dégâts aux autres :
#    - Les dégâts sont soustraits de la Santé. Si la Santé <= 0, le personnage meurt.
# 3. Un personnage peut en soigner un autre :
#    - Les personnages morts ne peuvent pas être soignés.
#    - Les soins ne peuvent pas faire dépasser la santé maximum (1000).
#
# -- Itération 2 --
# 1. Un personnage ne peut pas s'infliger de dégâts à lui-même.
# 2. Un personnage ne peut soigner QUE lui-même.
# 3. Lors d'une attaque :
#    - Si la cible a 5 niveaux (ou plus) de PLUS que l'attaquant, dégâts réduits de 50%.
#    - Si la cible a 5 niveaux (ou plus) de MOINS que l'attaquant, dégâts augmentés de 50%.
#
# -- Itération 3 --
# 1. Les personnages ont une portée d'attaque (Max Range).
# 2. Les combattants de mêlée (Melee) ont une portée de 2 mètres.
# 3. Les combattants à distance (Ranged) ont une portée de 20 mètres.
# 4. Il faut être à portée pour infliger des dégâts (on introduit une position X).
#
# -- Itération 4 --
# 1. Les personnages peuvent appartenir à une ou plusieurs Factions (aucune au départ).
# 2. Ils peuvent rejoindre ou quitter une Faction.
# 3. Les membres d'une même Faction sont des Alliés.
# 4. Les Alliés ne peuvent pas s'infliger de dégâts.
# 5. Les Alliés PEUVENT se soigner entre eux (modifie la règle de l'itération 2).
#
# -- Itération 5 --
# 1. Les personnages peuvent attaquer des objets du décor (Props, ex: un Arbre).
# 2. Les objets ont de la Santé. Ils ne peuvent ni soigner, ni attaquer, ni rejoindre
#    de factions. À 0 de Santé, ils sont Détruits.
# ==============================================================================

class GameObject:
    """Classe de base pour toute entité ayant de la santé sur le terrain."""
    def __init__(self, health, position=0):
        self.health = health
        self.max_health = health
        self.position = position

    @property
    def is_alive(self):
        return self.health > 0

    def receive_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

class Prop(GameObject):
    """Objet inanimé du décor (Arbre, Mur, etc.)"""
    pass

class Character(GameObject):
    """Personnage du jeu."""
    def __init__(self, attack_type='melee', position=0, level=1):
        super().__init__(health=1000, position=position)
        self.level = level
        self.attack_type = attack_type
        self.factions = set()

    @property
    def attack_range(self):
        return 20 if self.attack_type == 'ranged' else 2

    def join_faction(self, faction):
        self.factions.add(faction)

    def leave_faction(self, faction):
        self.factions.discard(faction)

    def is_ally(self, other):
        if not isinstance(other, Character):
            return False
        return not self.factions.isdisjoint(other.factions)

    def deal_damage(self, target, amount):
        # Règle : Ne peut pas s'attaquer soi-même
        if target is self:
            return
            
        # Règle : Les alliés ne peuvent pas s'attaquer
        if self.is_ally(target):
            return
            
        # Règle : Vérification de la portée
        distance = abs(self.position - target.position)
        if distance > self.attack_range:
            return

        # Règle : Modificateurs de niveau (uniquement entre personnages)
        actual_damage = amount
        if isinstance(target, Character):
            if target.level >= self.level + 5:
                actual_damage *= 0.5
            elif target.level <= self.level - 5:
                actual_damage *= 1.5

        target.receive_damage(actual_damage)

    def heal(self, target, amount):
        # Règle : Impossible de soigner un mort
        if not target.is_alive:
            return
            
        # Règle : Les objets ne peuvent pas être soignés
        if not isinstance(target, Character):
            return
            
        # Règle : Ne peut soigner que soi-même ou un allié
        if target is not self and not self.is_ally(target):
            return

        target.health += amount
        if target.health > target.max_health:
            target.health = target.max_health


# ==============================================================================
# TESTS UNITAIRES
# ==============================================================================

class TestRPGCombat(unittest.TestCase):

    def test_iteration_1_basics(self):
        p1 = Character()
        p2 = Character()
        
        self.assertEqual(p1.health, 1000)
        self.assertEqual(p1.level, 1)
        self.assertTrue(p1.is_alive)
        
        p1.deal_damage(p2, 100)
        self.assertEqual(p2.health, 900)
        
        # Test de la mort
        p1.deal_damage(p2, 1000)
        self.assertEqual(p2.health, 0)
        self.assertFalse(p2.is_alive)
        
        # Impossible de soigner un mort
        p1.heal(p2, 100)
        self.assertEqual(p2.health, 0)

    def test_iteration_2_self_harm_and_healing(self):
        p1 = Character()
        p2 = Character()
        
        # Pas d'auto-attaque
        p1.deal_damage(p1, 100)
        self.assertEqual(p1.health, 1000)
        
        p1.receive_damage(200)
        self.assertEqual(p1.health, 800)
        
        # Auto-soin autorisé
        p1.heal(p1, 50)
        self.assertEqual(p1.health, 850)
        
        # Ne peut pas dépasser le max
        p1.heal(p1, 500)
        self.assertEqual(p1.health, 1000)
        
        # Ne peut pas soigner un ennemi
        p1.heal(p2, 100)
        
    def test_iteration_2_level_modifiers(self):
        p_low = Character(level=1)
        p_high = Character(level=6)
        
        # Cible a 5 niveaux de plus : dégâts / 2
        p_low.deal_damage(p_high, 100)
        self.assertEqual(p_high.health, 950) 
        
        # Cible a 5 niveaux de moins : dégâts * 1.5
        p_high.deal_damage(p_low, 100)
        self.assertEqual(p_low.health, 850)

    def test_iteration_3_attack_range(self):
        melee = Character(attack_type='melee', position=0)
        ranged = Character(attack_type='ranged', position=0)
        target = Character(position=15)
        
        # Mêlée hors de portée
        melee.deal_damage(target, 100)
        self.assertEqual(target.health, 1000)
        
        # Ranged à portée
        ranged.deal_damage(target, 100)
        self.assertEqual(target.health, 900)

    def test_iteration_4_factions_and_allies(self):
        p1 = Character()
        p2 = Character()
        
        p1.join_faction("Elves")
        p2.join_faction("Elves")
        
        # Alliés : pas de dégâts
        p1.deal_damage(p2, 100)
        self.assertEqual(p2.health, 1000)
        
        # Alliés : peuvent se soigner
        p2.receive_damage(200)
        p1.heal(p2, 100)
        self.assertEqual(p2.health, 900)
        
        # Si quitte la faction, redeviennent ennemis
        p2.leave_faction("Elves")
        p1.deal_damage(p2, 100)
        self.assertEqual(p2.health, 800)

    def test_iteration_5_props(self):
        p1 = Character()
        tree = Prop(health=2000, position=0)
        
        # Peut attaquer un objet
        p1.deal_damage(tree, 500)
        self.assertEqual(tree.health, 1500)
        
        # Ne peut pas soigner un objet
        p1.heal(tree, 100)
        self.assertEqual(tree.health, 1500)
        
        # Destruction
        p1.deal_damage(tree, 2000)
        self.assertEqual(tree.health, 0)
        self.assertFalse(tree.is_alive)

if __name__ == '__main__':
    unittest.main()