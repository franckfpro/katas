import unittest
from datetime import datetime, timedelta

# =============================================================================
# CONSIGNES DU KATA : RED PENCIL SALE (PROMOTION CRAYON ROUGE)
# =============================================================================
# Vous devez implémenter les règles d'activation et de désactivation des 
# promotions "Crayon Rouge" pour un portail de vente en ligne.
#
# Règles métier :
# 1. Activation : Une promo démarre suite à une baisse de prix. La baisse 
#    doit être d'au moins 5% et d'au plus 30%. Le prix précédent doit être 
#    resté stable pendant au moins 30 jours.
# 2. Durée : La promotion dure au maximum 30 jours.
# 3. Réduction supplémentaire : Si le prix est encore réduit pendant la promo, 
#    celle-ci n'est PAS prolongée.
# 4. Augmentation : Si le prix augmente pendant la promo, celle-ci se termine 
#    immédiatement.
# 5. Limite de réduction : Si une réduction supplémentaire pendant la promo 
#    entraîne une baisse globale de plus de 30% par rapport au prix d'origine 
#    de la promo, celle-ci se termine immédiatement.
# 6. Promotions successives : Après la fin d'une promo, de nouvelles promos 
#    peuvent suivre. Cependant, la condition de départ s'applique : le prix 
#    doit être stable pendant 30 jours (et ces 30 jours ne peuvent pas 
#    intersecter une précédente promo "Crayon Rouge").
# =============================================================================

class Product:
    def __init__(self, initial_price: float, current_date: datetime):
        self.price = initial_price
        self.last_price_change_date = current_date
        
        # État de la promotion
        self.promo_active = False
        self.promo_start_date = None
        self.promo_original_price = None
        self.last_promo_end_date = None

    def change_price(self, new_price: float, change_date: datetime):
        """Modifie le prix du produit et réévalue l'état de la promotion."""
        if new_price == self.price:
            return

        # Vérifier d'abord si la promo a expiré avec le temps écoulé
        self._update_promo_state(change_date)

        if self.promo_active:
            if new_price > self.price:
                # Règle 4 : Augmentation du prix = fin immédiate
                self._end_promo(change_date)
            else:
                # Règle 3 & 5 : Baisse supplémentaire
                overall_discount = (self.promo_original_price - new_price) / self.promo_original_price
                if overall_discount > 0.30:
                    # Fin immédiate si on dépasse 30% de remise globale
                    self._end_promo(change_date)
                # Sinon la promo continue (sans être prolongée)
        else:
            # Règle 1 & 6 : Tentative de démarrage d'une promo
            stable_start = self.last_price_change_date
            
            # Les 30 jours de stabilité ne peuvent pas chevaucher une promo précédente
            if self.last_promo_end_date and self.last_promo_end_date > stable_start:
                stable_start = self.last_promo_end_date

            days_stable = (change_date - stable_start).days

            if days_stable >= 30:
                if new_price < self.price:
                    discount = (self.price - new_price) / self.price
                    # round() pour éviter les erreurs de précision sur les flottants
                    if 0.05 <= round(discount, 4) <= 0.30:
                        self.promo_active = True
                        self.promo_start_date = change_date
                        self.promo_original_price = self.price

        self.price = new_price
        self.last_price_change_date = change_date

    def is_red_pencil(self, current_date: datetime) -> bool:
        """Retourne True si le produit est actuellement en promotion Crayon Rouge."""
        self._update_promo_state(current_date)
        return self.promo_active

    def _update_promo_state(self, current_date: datetime):
        """Désactive la promotion si la durée de 30 jours est dépassée."""
        if self.promo_active and (current_date - self.promo_start_date).days > 30:
            # Règle 2 : La promo expire exactement 30 jours après son début
            self._end_promo(self.promo_start_date + timedelta(days=30))

    def _end_promo(self, end_date: datetime):
        """Met fin à la promotion en cours et sauvegarde la date de fin."""
        self.promo_active = False
        self.last_promo_end_date = end_date
        self.promo_start_date = None
        self.promo_original_price = None


# =============================================================================
# TESTS UNITAIRES
# =============================================================================
class TestRedPencilSale(unittest.TestCase):

    def setUp(self):
        self.start_date = datetime(2023, 1, 1)
        self.product = Product(100.0, self.start_date)

    def test_promo_starts_if_valid_discount_after_30_days_stable(self):
        # 30 jours plus tard, baisse de 20%
        change_date = self.start_date + timedelta(days=30)
        self.product.change_price(80.0, change_date)
        
        self.assertTrue(self.product.is_red_pencil(change_date))

    def test_promo_does_not_start_if_discount_less_than_5_percent(self):
        change_date = self.start_date + timedelta(days=30)
        self.product.change_price(96.0, change_date) # Baisse de 4%
        
        self.assertFalse(self.product.is_red_pencil(change_date))

    def test_promo_does_not_start_if_discount_more_than_30_percent(self):
        change_date = self.start_date + timedelta(days=30)
        self.product.change_price(60.0, change_date) # Baisse de 40%
        
        self.assertFalse(self.product.is_red_pencil(change_date))

    def test_promo_does_not_start_if_price_unstable(self):
        # Changement mineur jour 15
        unstable_date = self.start_date + timedelta(days=15)
        self.product.change_price(99.0, unstable_date)
        
        # Vraie baisse jour 30 (mais seulement 15 jours de stabilité depuis le dernier changement)
        change_date = self.start_date + timedelta(days=30)
        self.product.change_price(80.0, change_date)
        
        self.assertFalse(self.product.is_red_pencil(change_date))

    def test_promo_ends_after_30_days(self):
        promo_start = self.start_date + timedelta(days=30)
        self.product.change_price(80.0, promo_start)
        
        self.assertTrue(self.product.is_red_pencil(promo_start + timedelta(days=15)))
        self.assertFalse(self.product.is_red_pencil(promo_start + timedelta(days=31)))

    def test_promo_not_prolonged_by_further_reduction(self):
        promo_start = self.start_date + timedelta(days=30)
        self.product.change_price(80.0, promo_start) # -20%
        
        # 15 jours plus tard, nouvelle baisse qui reste < 30% au global (-25%)
        further_reduction = promo_start + timedelta(days=15)
        self.product.change_price(75.0, further_reduction) 
        
        # La promo doit toujours expirer à J+30 depuis le DÉBUT de la promo (pas J+45)
        self.assertFalse(self.product.is_red_pencil(promo_start + timedelta(days=31)))

    def test_promo_ends_immediately_if_price_increases(self):
        promo_start = self.start_date + timedelta(days=30)
        self.product.change_price(80.0, promo_start)
        
        increase_date = promo_start + timedelta(days=10)
        self.product.change_price(85.0, increase_date)
        
        self.assertFalse(self.product.is_red_pencil(increase_date))

    def test_promo_ends_if_overall_discount_exceeds_30_percent(self):
        promo_start = self.start_date + timedelta(days=30)
        self.product.change_price(80.0, promo_start) # -20%
        
        # Baisse supplémentaire menant le prix à 65.0 (-35% global depuis 100.0)
        huge_drop_date = promo_start + timedelta(days=10)
        self.product.change_price(65.0, huge_drop_date)
        
        self.assertFalse(self.product.is_red_pencil(huge_drop_date))

    def test_subsequent_promo_requires_30_days_stability_after_previous_ends(self):
        # Promo 1
        promo_start = self.start_date + timedelta(days=30)
        self.product.change_price(80.0, promo_start)
        
        # Promo 1 expire à J+60 (30 + 30)
        promo_end = promo_start + timedelta(days=30)
        self.assertFalse(self.product.is_red_pencil(promo_end + timedelta(days=1)))
        
        # Essai de promo 2 à J+70 (seulement 10 jours depuis la fin de la promo 1)
        invalid_promo_2_date = promo_end + timedelta(days=10)
        self.product.change_price(70.0, invalid_promo_2_date)
        self.assertFalse(self.product.is_red_pencil(invalid_promo_2_date))
        
        # Essai de promo 3 valide : 30 jours après la baisse à J+70
        valid_promo_3_date = invalid_promo_2_date + timedelta(days=30)
        self.product.change_price(60.0, valid_promo_3_date)
        self.assertTrue(self.product.is_red_pencil(valid_promo_3_date))

if __name__ == '__main__':
    unittest.main()