import os
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, mock_open

# ==============================================================================
# CONSIGNES DU KATA : FILE LOGGER
# ==============================================================================
# Contexte :
# Ce kata est conçu pour aider à développer des compétences dans l'utilisation
# appropriée des objets Mock (simulacres). Les premières étapes peuvent être 
# réalisées de manière basique, mais les dernières deviennent très difficiles 
# sans la capacité de simuler (mocker) certaines dépendances (Temps, Fichiers).
#
# Instructions (implémentées dans leur état final ci-dessous) :
# 1. Créez une classe 'FileLogger' avec une méthode 'log(message: str)'.
# 2. La méthode ajoute le message à la fin d'un fichier (ex: "log.txt").
# 3. Les messages doivent être préfixés par "YYYY-MM-DD HH:MM:SS " (heure locale).
# 4. Si le fichier n'existe pas, il est créé. Sinon, on ajoute à la fin.
# 5. Modifiez la méthode pour écrire dans "logYYYYMMDD.txt" selon la date du jour.
# 6. Vérifiez qu'un nouveau fichier est créé à chaque nouveau jour.
# 7. Les samedis et dimanches, écrivez plutôt dans "weekend.txt".
# 8. Lors du premier log d'un NOUVEAU week-end, renommez l'ancien "weekend.txt" 
#    en "weekend-YYYYMMDD.txt" (où YYYYMMDD correspond au samedi de cet ancien 
#    week-end) avant de recommencer un fichier "weekend.txt" tout neuf.
# ==============================================================================


class FileLogger:
    def __init__(self, time_provider=None):
        """
        Initialise le logger.
        L'injection de 'time_provider' permet de contrôler le temps dans les tests.
        """
        self.time_provider = time_provider or datetime.now

    def _get_saturday_of_weekend(self, dt: datetime) -> datetime:
        """
        Retourne la date du samedi correspondant au week-end de la date fournie.
        Retourne None si la date n'est pas un week-end.
        """
        if dt.weekday() == 5:  # Samedi
            return dt
        elif dt.weekday() == 6:  # Dimanche
            return dt - timedelta(days=1)
        return None

    def log(self, message: str):
        """
        Enregistre un message dans le fichier approprié selon les règles métier.
        """
        now = self.time_provider()
        timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"{timestamp_str} {message}\n"
        
        is_weekend = now.weekday() in (5, 6) # 5 = Samedi, 6 = Dimanche
        
        if is_weekend:
            filename = "weekend.txt"
            
            # Gestion de la rotation des fichiers du week-end (Étape 8)
            if os.path.exists(filename):
                mtime = os.path.getmtime(filename)
                file_dt = datetime.fromtimestamp(mtime)
                
                file_saturday = self._get_saturday_of_weekend(file_dt)
                current_saturday = self._get_saturday_of_weekend(now)
                
                # Si le fichier date d'un week-end précédent, on le renomme
                if file_saturday and current_saturday and (file_saturday.date() != current_saturday.date()):
                    old_filename = f"weekend-{file_saturday.strftime('%Y%m%d')}.txt"
                    os.rename(filename, old_filename)
        else:
            # En semaine, on crée un fichier par jour (Étape 5)
            filename = f"log{now.strftime('%Y%m%d')}.txt"
            
        # Écriture dans le fichier (append)
        with open(filename, "a") as f:
            f.write(formatted_message)


# ==============================================================================
# TESTS UNITAIRES
# ==============================================================================

class TestFileLogger(unittest.TestCase):

    def test_log_on_weekday_writes_to_daily_file_with_correct_format(self):
        # Lundi 3 Février 2020, 10:25:23
        mock_time = datetime(2020, 2, 3, 10, 25, 23)
        logger = FileLogger(time_provider=lambda: mock_time)
        
        # On intercepte la fonction built-in `open`
        with patch("builtins.open", mock_open()) as mocked_file:
            # On intercepte `os.path.exists` pour renvoyer False par défaut
            with patch("os.path.exists", return_value=False):
                logger.log("test message")
                
                # Vérification du nom de fichier généré (Étape 5)
                mocked_file.assert_called_once_with("log20200203.txt", "a")
                
                # Vérification du formatage du message (Étape 3)
                mocked_file().write.assert_called_once_with("2020-02-03 10:25:23 test message\n")

    def test_log_on_weekend_writes_to_weekend_file(self):
        # Samedi 1er Février 2020, 12:00:00
        mock_time = datetime(2020, 2, 1, 12, 0, 0)
        logger = FileLogger(time_provider=lambda: mock_time)
        
        with patch("builtins.open", mock_open()) as mocked_file:
            with patch("os.path.exists", return_value=False):
                logger.log("weekend start")
                
                # Vérification du nom de fichier pour le week-end (Étape 7)
                mocked_file.assert_called_once_with("weekend.txt", "a")
                mocked_file().write.assert_called_once_with("2020-02-01 12:00:00 weekend start\n")

    @patch("os.rename")
    @patch("os.path.getmtime")
    @patch("os.path.exists")
    def test_weekend_file_rollover_on_new_weekend(self, mock_exists, mock_getmtime, mock_rename):
        # Contexte : Nous sommes le Samedi 8 Février 2020
        mock_time = datetime(2020, 2, 8, 14, 0, 0)
        logger = FileLogger(time_provider=lambda: mock_time)
        
        # Le fichier "weekend.txt" existe déjà
        mock_exists.return_value = True
        
        # Le fichier existant a été modifié le Dimanche 2 Février 2020 (Week-end précédent)
        old_weekend_time = datetime(2020, 2, 2, 10, 0, 0)
        mock_getmtime.return_value = old_weekend_time.timestamp()
        
        with patch("builtins.open", mock_open()) as mocked_file:
            logger.log("new weekend message")
            
            # On vérifie que l'ancien fichier a été renommé avec la date du SAMEDI précédent (1er Février) (Étape 8)
            mock_rename.assert_called_once_with("weekend.txt", "weekend-20200201.txt")
            
            # On vérifie qu'on écrit bien dans le (nouveau) fichier "weekend.txt"
            mocked_file.assert_called_once_with("weekend.txt", "a")

    @patch("os.rename")
    @patch("os.path.getmtime")
    @patch("os.path.exists")
    def test_weekend_file_does_not_rollover_during_same_weekend(self, mock_exists, mock_getmtime, mock_rename):
        # Contexte : Nous sommes le Dimanche 2 Février 2020
        mock_time = datetime(2020, 2, 2, 14, 0, 0)
        logger = FileLogger(time_provider=lambda: mock_time)
        
        mock_exists.return_value = True
        
        # Le fichier existant a été créé la veille : Samedi 1er Février 2020
        same_weekend_time = datetime(2020, 2, 1, 10, 0, 0)
        mock_getmtime.return_value = same_weekend_time.timestamp()
        
        with patch("builtins.open", mock_open()) as mocked_file:
            logger.log("same weekend message")
            
            # On vérifie qu'AUCUN renommage n'a lieu car on est sur le même week-end
            mock_rename.assert_not_called()
            mocked_file.assert_called_once_with("weekend.txt", "a")


if __name__ == '__main__':
    unittest.main()