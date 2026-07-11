import unittest

"""
KATA GILDED ROSE

Description du problème :
Vous gérez l'inventaire d'une auberge. Chaque jour, les valeurs SellIn (jours restants) 
et Quality (valeur de l'objet) diminuent. Votre tâche est d'ajouter une nouvelle 
catégorie d'objets ("Conjured") sans casser les règles existantes, et sans 
modifier la classe `Item` d'origine.

Règles de calcul :
- Fin de journée : SellIn et Quality diminuent de 1.
- Après péremption (SellIn < 0) : Quality diminue deux fois plus vite.
- Quality est toujours >= 0 et <= 50.
- "Aged Brie" augmente en Quality au fil du temps.
- "Sulfuras" est légendaire : Quality = 80, ne se périme jamais, ne baisse jamais.
- "Backstage passes" : Quality +2 si SellIn <= 10, +3 si SellIn <= 5, tombe à 0 si SellIn < 0.
- NOUVEAU : "Conjured" diminue en Quality deux fois plus vite qu'un objet normal.

Contrainte stricte :
NE PAS MODIFIER la classe Item.
"""

# --- CODE LÉGACY (NE PAS MODIFIER CETTE CLASSE) ---

class Item:
    def __init__(self, name: str, sell_in: int, quality: int):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

# --- SOLUTION REFACTORISÉE ---

class GildedRose:
    def __init__(self, items: list[Item]):
        self.items = items

    def update_quality(self):
        """Met à jour l'inventaire complet."""
        for item in self.items:
            self._update_item(item)

    def _update_item(self, item: Item):
        """Détermine la logique de mise à jour selon le type d'objet."""
        
        # Sulfuras ne change jamais
        if item.name == "Sulfuras, Hand of Ragnaros":
            return

        # Tous les autres objets vieillissent d'un jour
        item.sell_in -= 1

        # Application de la logique spécifique par nom
        if item.name == "Aged Brie":
            self._update_aged_brie(item)
        elif item.name == "Backstage passes to a TAFKAL80ETC concert":
            self._update_backstage_passes(item)
        elif "Conjured" in item.name:
            self._update_conjured(item)
        else:
            self._update_normal_item(item)

    # --- Méthodes d'aide pour isoler la logique métier ---

    def _update_normal_item(self, item: Item):
        self._decrease_quality(item, 1)
        if item.sell_in < 0:
            self._decrease_quality(item, 1)

    def _update_aged_brie(self, item: Item):
        self._increase_quality(item)
        if item.sell_in < 0:
            self._increase_quality(item)

    def _update_backstage_passes(self, item: Item):
        self._increase_quality(item)
        if item.sell_in < 10:
            self._increase_quality(item)
        if item.sell_in < 5:
            self._increase_quality(item)
        if item.sell_in < 0:
            item.quality = 0

    def _update_conjured(self, item: Item):
        self._decrease_quality(item, 2)
        if item.sell_in < 0:
            self._decrease_quality(item, 2)

    def _increase_quality(self, item: Item):
        """Augmente la qualité sans dépasser la limite de 50."""
        if item.quality < 50:
            item.quality += 1

    def _decrease_quality(self, item: Item, amount: int):
        """Diminue la qualité sans descendre sous 0."""
        item.quality = max(0, item.quality - amount)


# --- TESTS UNITAIRES ---

class TestGildedRose(unittest.TestCase):
    
    def _update_single_item(self, name: str, sell_in: int, quality: int) -> Item:
        """Fonction utilitaire pour tester un objet de manière isolée."""
        items = [Item(name, sell_in, quality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        return items[0]

    def test_normal_item_before_sell_date(self):
        item = self._update_single_item("Normal Item", 10, 20)
        self.assertEqual(item.sell_in, 9)
        self.assertEqual(item.quality, 19)

    def test_normal_item_on_sell_date(self):
        item = self._update_single_item("Normal Item", 0, 20)
        self.assertEqual(item.sell_in, -1)
        self.assertEqual(item.quality, 18) # Se dégrade 2x plus vite

    def test_normal_item_quality_never_negative(self):
        item = self._update_single_item("Normal Item", 10, 0)
        self.assertEqual(item.quality, 0)

    def test_aged_brie_increases_in_quality(self):
        item = self._update_single_item("Aged Brie", 2, 0)
        self.assertEqual(item.quality, 1)

    def test_aged_brie_quality_never_exceeds_50(self):
        item = self._update_single_item("Aged Brie", 2, 50)
        self.assertEqual(item.quality, 50)

    def test_sulfuras_never_changes(self):
        item = self._update_single_item("Sulfuras, Hand of Ragnaros", 0, 80)
        self.assertEqual(item.sell_in, 0)
        self.assertEqual(item.quality, 80)

    def test_backstage_passes_more_than_10_days(self):
        item = self._update_single_item("Backstage passes to a TAFKAL80ETC concert", 15, 20)
        self.assertEqual(item.quality, 21)

    def test_backstage_passes_10_days_or_less(self):
        item = self._update_single_item("Backstage passes to a TAFKAL80ETC concert", 10, 20)
        self.assertEqual(item.quality, 22)

    def test_backstage_passes_5_days_or_less(self):
        item = self._update_single_item("Backstage passes to a TAFKAL80ETC concert", 5, 20)
        self.assertEqual(item.quality, 23)

    def test_backstage_passes_after_concert(self):
        item = self._update_single_item("Backstage passes to a TAFKAL80ETC concert", 0, 20)
        self.assertEqual(item.quality, 0)

    def test_conjured_item_before_sell_date(self):
        item = self._update_single_item("Conjured Mana Cake", 10, 20)
        self.assertEqual(item.quality, 18) # Se dégrade de 2 au lieu de 1

    def test_conjured_item_after_sell_date(self):
        item = self._update_single_item("Conjured Mana Cake", 0, 20)
        self.assertEqual(item.quality, 16) # Se dégrade de 4 (2 * 2x plus vite)

if __name__ == '__main__':
    unittest.main()