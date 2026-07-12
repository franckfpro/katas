import unittest

"""
KATA CHRISTMAS DELIVERY

Description du problème :
Vous devez concevoir le nouveau système de livraison du Père Noël géré par la Mère Noël.

User Story 1 : Un lutin prend un cadeau, le charge sur le traîneau (ce qui l'occupe), puis redevient disponible.
User Story 2 : La Mère Noël reçoit les cadeaux des machines et les distribue aux lutins libres. 
               Si tous sont occupés, elle met les cadeaux en attente.
User Story 3 : Optimisation. La Mère Noël doit essayer de grouper les cadeaux par famille 
               lorsqu'elle les donne aux lutins, sans pour autant laisser un lutin inactif.
User Story 4 : Le Père Noël peut signaler des familles "méchantes". Leurs cadeaux 
               doivent être détruits/ignorés par la Mère Noël.
"""

class Cadeau:
    def __init__(self, id_cadeau: str, famille: str):
        self.id_cadeau = id_cadeau
        self.famille = famille

    def __repr__(self):
        return f"Cadeau({self.id_cadeau}, Famille: {self.famille})"


class Traineau:
    def __init__(self):
        self.cargaison = []

    def ajouter_cadeau(self, cadeau: Cadeau):
        self.cargaison.append(cadeau)


class Lutin:
    def __init__(self, nom: str):
        self.nom = nom
        self.cadeau_en_cours = None

    @property
    def est_disponible(self) -> bool:
        return self.cadeau_en_cours is None

    def prendre_cadeau(self, cadeau: Cadeau):
        self.cadeau_en_cours = cadeau

    def deposer_sur_traineau(self, traineau: Traineau):
        if self.cadeau_en_cours:
            traineau.ajouter_cadeau(self.cadeau_en_cours)
            self.cadeau_en_cours = None


class MereNoel:
    def __init__(self, traineau: Traineau, lutins: list[Lutin]):
        self.traineau = traineau
        self.lutins = lutins
        self.file_attente = []
        self.familles_mechantes = set()
        self.derniere_famille_en_cours = None

    def signaler_famille_mechante(self, famille: str):
        """US 4: Marque une famille comme méchante et retire ses cadeaux de la file."""
        self.familles_mechantes.add(famille)
        self.file_attente = [c for c in self.file_attente if c.famille != famille]

    def recevoir_de_la_machine(self, cadeau: Cadeau):
        """US 2 & 4: Reçoit un cadeau, l'ignore si la famille est méchante, sinon le stocke."""
        if cadeau.famille not in self.familles_mechantes:
            self.file_attente.append(cadeau)
        self.assigner_cadeaux()

    def assigner_cadeaux(self):
        """US 3: Assigne les cadeaux en attente aux lutins disponibles avec stratégie de groupement."""
        lutins_libres = [l for l in self.lutins if l.est_disponible]

        while lutins_libres and self.file_attente:
            lutin = lutins_libres.pop(0)
            cadeau_a_assigner = None

            # Stratégie : Essayer de trouver un cadeau de la même famille que le précédent
            if self.derniere_famille_en_cours:
                for cadeau in self.file_attente:
                    if cadeau.famille == self.derniere_famille_en_cours:
                        cadeau_a_assigner = cadeau
                        break
            
            # Si aucun cadeau de la même famille n'est trouvé, on prend le premier de la file
            if not cadeau_a_assigner:
                cadeau_a_assigner = self.file_attente[0]

            self.file_attente.remove(cadeau_a_assigner)
            lutin.prendre_cadeau(cadeau_a_assigner)
            self.derniere_famille_en_cours = cadeau_a_assigner.famille

    def faire_travailler_les_lutins(self):
        """Simule le passage du temps : les lutins occupés déposent leurs cadeaux."""
        for lutin in self.lutins:
            if not lutin.est_disponible:
                lutin.deposer_sur_traineau(self.traineau)
        
        # Une fois les lutins libres, on tente de leur réassigner de nouveaux cadeaux
        self.assigner_cadeaux()


# --- TESTS UNITAIRES ---

class TestChristmasDelivery(unittest.TestCase):

    def setUp(self):
        self.traineau = Traineau()
        self.lutin1 = Lutin("Alabaster")
        self.lutin2 = Lutin("Bushy")
        self.mere_noel = MereNoel(self.traineau, [self.lutin1, self.lutin2])

    def test_us1_et_us2_distribution_simple(self):
        """Teste qu'un cadeau reçu est donné à un lutin, puis déposé sur le traîneau."""
        cadeau = Cadeau("1", "Dupont")
        
        self.mere_noel.recevoir_de_la_machine(cadeau)
        
        # Le lutin 1 a pris le cadeau, la file est vide
        self.assertFalse(self.lutin1.est_disponible)
        self.assertEqual(len(self.mere_noel.file_attente), 0)
        self.assertEqual(len(self.traineau.cargaison), 0)

        # Le temps passe... le lutin dépose le cadeau
        self.mere_noel.faire_travailler_les_lutins()
        self.assertTrue(self.lutin1.est_disponible)
        self.assertEqual(len(self.traineau.cargaison), 1)

    def test_us2_mise_en_attente(self):
        """Teste que les cadeaux sont mis en attente si tous les lutins sont occupés."""
        # 3 cadeaux pour 2 lutins
        self.mere_noel.recevoir_de_la_machine(Cadeau("1", "Dupont"))
        self.mere_noel.recevoir_de_la_machine(Cadeau("2", "Martin"))
        self.mere_noel.recevoir_de_la_machine(Cadeau("3", "Durand"))

        self.assertFalse(self.lutin1.est_disponible)
        self.assertFalse(self.lutin2.est_disponible)
        self.assertEqual(len(self.mere_noel.file_attente), 1) # Le 3ème attend
        
        # Les lutins finissent leur premier voyage
        self.mere_noel.faire_travailler_les_lutins()
        
        # Le traîneau a 2 cadeaux, le lutin 1 a récupéré le cadeau en attente
        self.assertEqual(len(self.traineau.cargaison), 2)
        self.assertFalse(self.lutin1.est_disponible)
        self.assertEqual(len(self.mere_noel.file_attente), 0)

    def test_us3_optimisation_par_famille(self):
        """Teste la stratégie de groupement des cadeaux d'une même famille."""
        # On sature volontairement les lutins pour remplir la file d'attente
        self.lutin1.prendre_cadeau(Cadeau("X", "Bouchard"))
        self.lutin2.prendre_cadeau(Cadeau("Y", "Bouchard"))

        # Arrivée désordonnée de cadeaux
        self.mere_noel.recevoir_de_la_machine(Cadeau("1", "Famille_A"))
        self.mere_noel.recevoir_de_la_machine(Cadeau("2", "Famille_B"))
        self.mere_noel.recevoir_de_la_machine(Cadeau("3", "Famille_A"))

        # Les lutins finissent, ils vont piocher dans la file d'attente
        self.mere_noel.faire_travailler_les_lutins()

        # Le lutin 1 aurait dû prendre "1" (Famille A) 
        # Le lutin 2 aurait dû prendre "3" (Famille A) au lieu de "2" (Famille B) grâce à l'optimisation
        self.assertEqual(self.lutin1.cadeau_en_cours.id_cadeau, "1")
        self.assertEqual(self.lutin2.cadeau_en_cours.id_cadeau, "3")
        
        # Le cadeau de la Famille_B est resté en attente
        self.assertEqual(self.mere_noel.file_attente[0].famille, "Famille_B")

    def test_us4_familles_mechantes(self):
        """Teste que les cadeaux des familles méchantes sont jetés/ignorés."""
        self.mere_noel.signaler_famille_mechante("Grinch")

        self.mere_noel.recevoir_de_la_machine(Cadeau("1", "Grinch"))
        self.mere_noel.recevoir_de_la_machine(Cadeau("2", "Dupont"))

        # Seul le cadeau Dupont a été assigné au lutin 1
        self.assertFalse(self.lutin1.est_disponible)
        self.assertEqual(self.lutin1.cadeau_en_cours.famille, "Dupont")
        
        # Le cadeau Grinch n'a jamais été mis en file ou donné
        self.assertTrue(self.lutin2.est_disponible)


if __name__ == '__main__':
    unittest.main()