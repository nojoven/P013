import os
import fnmatch
from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Publication
from friendship.models import Follow
from unittest.mock import patch, call


class TestSetupStaysCommand(TestCase):
    def test_setup_stays(self):
        # Set an environment variable to indicate that the command is being run from a test
        os.environ["RUNNING_FROM_TEST"] = "1"

        # Exécution de la commande
        call_command("setupstays")

        # Vérification que 3 profils ont été créés
        User = get_user_model()
        self.assertEqual(User.objects.count(), 4)

        # Vérification que 12 publications ont été créées
        self.assertEqual(Publication.objects.count(), 12)

        # Vérification que chaque profil suit les autres

        self.assertEqual(Follow.objects.count(), 12)

        # Get the actual follow relationships
        actual_follows = [
            (f.follower_id, f.followee_id)
            for f in Follow.objects.all().order_by("follower_id", "followee_id")
        ]

        # Define the expected follow relationships
        expected_follows = [
            (1, 2),
            (1, 3),
            (1, 4),
            (2, 1),
            (2, 3),
            (2, 4),
            (3, 1),
            (3, 2),
            (3, 4),
            (4, 1),
            (4, 2),
            (4, 3),
        ]

        # Assert that the actual follow relationships match the expected ones
        self.assertListEqual(actual_follows, expected_follows)

        self.assertTrue(User.objects.filter(is_superuser=True).exists())

        # Remove the environment variable
        del os.environ["RUNNING_FROM_TEST"]


class TestRunTestsCommand(TestCase):
    @patch("subprocess.run")
    def test_runtests(self, mock_run):
        # Run the command
        call_command("runtests")

        # Check that subprocess.run was called with the expected arguments
        apps = ["core", "users", "locations", "stays"]
        expected_calls = []
        for app in apps:
            for dirpath, dirnames, filenames in os.walk(f"{app}/tests"):
                for filename in fnmatch.filter(filenames, "test_*.py"):
                    test_file = os.path.join(dirpath, filename)
                    expected_calls.append(
                        call(
                            ["pytest", "--cov=.", "--cov-append", test_file, "-s", "-v"]
                        )
                    )
        mock_run.assert_has_calls(expected_calls, any_order=True)
