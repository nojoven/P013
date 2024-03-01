
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
        os.environ['RUNNING_FROM_TEST'] = '1'

        # Exécution de la commande
        call_command('setupstays')

        # Vérification que 3 profils ont été créés
        User = get_user_model()
        self.assertEqual(User.objects.count(), 3)

        # Vérification que 12 publications ont été créées
        self.assertEqual(Publication.objects.count(), 12)

        # Vérification que chaque profil suit les autres
        users = User.objects.all()
        for user in users:
            # self.assertEqual(user.following.count(), 2)
            self.assertEqual(len(Follow.objects.following(user)), 2)
            self.assertEqual(len(Follow.objects.followers(user)), 2)

        # Remove the environment variable
        del os.environ['RUNNING_FROM_TEST']



class TestRunTestsCommand(TestCase):
    @patch('subprocess.run')
    def test_runtests(self, mock_run):
        # Run the command
        call_command('runtests')

        # Check that subprocess.run was called with the expected arguments
        apps = ['core', 'users', 'locations', 'stays']
        expected_calls = []
        for app in apps:
            for dirpath, dirnames, filenames in os.walk(f'{app}/tests'):
                for filename in fnmatch.filter(filenames, 'test_*.py'):
                    test_file = os.path.join(dirpath, filename)
                    expected_calls.append(call(['pytest', '--cov=.', '--cov-append', test_file, '-s', '-v']))
        mock_run.assert_has_calls(expected_calls, any_order=True)
