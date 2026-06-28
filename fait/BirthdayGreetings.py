import unittest
from unittest.mock import MagicMock, call
from typing import Protocol, List
from dataclasses import dataclass
from datetime import date

# =============================================================================
# KATA : Birthday Greetings
# =============================================================================
#
# CONSIGNES :
#
# Comme vous êtes une personne très amicale, vous aimeriez envoyer un petit
# mot d'anniversaire à tous vos amis. Mais vous avez beaucoup d'amis et vous
# êtes un peu paresseux, cela prendrait trop de temps de tout écrire à la main.
# La bonne nouvelle, c'est que les ordinateurs peuvent le faire pour vous.
#
# Imaginez que vous avez un fichier plat avec tous vos amis :
# last_name, first_name, date_of_birth, email
# Doe, John, 1982/10/08, john.doe@foobar.com
# Ann, Mary, 1975/09/11, mary.ann@foobar.com
#
# Et vous voulez leur envoyer un email de joyeux anniversaire le jour J :
# Sujet : Happy birthday!
# Message : Happy birthday, dear <first_name>!
#
# Comment concevoir ce logiciel ? Essayez de l'implémenter de manière à
# pouvoir facilement changer :
# - la façon de récupérer les données (ex: passer à une base SQLite)
# - la façon d'envoyer le message (ex: envoyer un SMS au lieu d'un email)
#
# Quel genre de tests écririez-vous ? Utiliseriez-vous des Mocks ?
#
# FONCTIONNALITÉS SUPPLÉMENTAIRES (Bonus) :
# - Les amis nés un 29 Février doivent être fêtés le 28 Février (les années non bissextiles).
# - Envoyer un rappel d'anniversaire aux autres amis :
#   Sujet : Birthday Reminder
#   Message : Dear <first_name>, Today is <someone_else_first_name> <someone_else_last_name>'s birthday. Don't forget to send him a message !
# - Envoyer un rappel groupé s'il y a plusieurs anniversaires :
#   Message : Today is <full_name_1>, <full_name_2> and <full_name_3>'s birthday...
# =============================================================================


@dataclass
class Friend:
    last_name: str
    first_name: str
    date_of_birth: date
    email: str


class FriendRepository(Protocol):
    """Interface (Port) pour l'accès aux données des amis."""

    def get_all_friends(self) -> List[Friend]: ...


class NotificationService(Protocol):
    """Interface (Port) pour l'envoi de messages."""

    def send_greeting(self, friend: Friend) -> None: ...

    def send_reminder(
        self, recipient: Friend, birthday_friends: List[Friend]
    ) -> None: ...


class BirthdayService:
    """
    Cas d'usage principal. Orchestre la récupération des données
    et l'envoi des notifications.
    """

    def __init__(self, repository: FriendRepository, notifier: NotificationService):
        self.repository = repository
        self.notifier = notifier

    def send_greetings(self, today: date) -> None:
        """
        Envoie les vœux d'anniversaire à tous les amis nés aujourd'hui.
        """
        # TODO : Implémenter la logique de récupération, de vérification de la date
        # (incluant la gestion du 29 Février) et l'envoi via self.notifier.
        for friend in self.repository.get_all_friends():
            if (
                friend.date_of_birth.year % 4 == 0
                and friend.date_of_birth.day == 29
                and friend.date_of_birth.month == 2
                and today.month == 2
                and today.day == 28
            ):
                self.notifier.send_greeting(friend)
            if (
                today.month == friend.date_of_birth.month
                and today.day == friend.date_of_birth.day
            ):
                self.notifier.send_greeting(friend)


# =============================================================================
# TESTS UNITAIRES
# =============================================================================


class TestBirthdayService(unittest.TestCase):

    def setUp(self):
        # Utilisation de Mocks pour isoler la logique métier des implémentations techniques
        self.mock_repository = MagicMock(spec=FriendRepository)
        self.mock_notifier = MagicMock(spec=NotificationService)
        self.service = BirthdayService(self.mock_repository, self.mock_notifier)

    def test_sends_greetings_to_friends_born_today(self):
        # Arrange
        today = date(2026, 10, 8)
        john = Friend("Doe", "John", date(1982, 10, 8), "john.doe@foobar.com")
        mary = Friend("Ann", "Mary", date(1975, 9, 11), "mary.ann@foobar.com")

        self.mock_repository.get_all_friends.return_value = [john, mary]

        # Act
        self.service.send_greetings(today)

        # Assert
        # Vérifie que la notification a bien été appelée uniquement pour John
        self.mock_notifier.send_greeting.assert_called_once_with(john)
        self.assertNotIn(call(mary), self.mock_notifier.send_greeting.mock_calls)

    def test_does_not_send_greetings_when_nobody_is_born_today(self):
        # Arrange
        today = date(2026, 1, 1)
        john = Friend("Doe", "John", date(1982, 10, 8), "john.doe@foobar.com")

        self.mock_repository.get_all_friends.return_value = [john]

        # Act
        self.service.send_greetings(today)

        # Assert
        self.mock_notifier.send_greeting.assert_not_called()

    # =========================================================================
    # TESTS POUR LES FONCTIONNALITÉS SUPPLÉMENTAIRES (À dé-commenter)
    # =========================================================================

    def test_handles_leap_year_birthdays_on_non_leap_years(self):
        # Arrange
        today_non_leap = date(2026, 2, 28)
        leap_year_friend = Friend("Leap", "Bob", date(1996, 2, 29), "bob@leap.com")
        self.mock_repository.get_all_friends.return_value = [leap_year_friend]

        # Act
        self.service.send_greetings(today_non_leap)

        # Assert
        self.mock_notifier.send_greeting.assert_called_once_with(leap_year_friend)


if __name__ == "__main__":
    unittest.main(verbosity=2)
#    class FriendRepositoryBis:
#        def __init__(self, friends):
#            self.friends = friends
#
#        def get_all_friends(self) -> List[Friend]:
#            return self.friends
#
#    class NotificationServiceBis:
#        def __init__(self, friend):
#            self.friend = friend
#
#        def send_greeting(self, friend: Friend) -> None:
#            print(f"anniv {friend.first_name}")
#
#        def send_reminder(
#            self, recipient: Friend, birthday_friends: List[Friend]
#        ) -> None: ...
#
#    notif = NotificationServiceBis(Friend)
#    friends = FriendRepositoryBis(
#        [
#            Friend("Doe", "John", date(1982, 10, 8), "john.doe@foobar.com"),
#            Friend("Ann", "Mary", date(1975, 9, 11), "mary.ann@foobar.com"),
#        ]
#    )
#    today = date(2026, 10, 8)
#    service = BirthdayService(friends, notif)
#    service.send_greetings(today)
