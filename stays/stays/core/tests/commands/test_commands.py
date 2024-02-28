
from django_q.models import OrmQ
from datetime import datetime, timedelta
from io import StringIO
from django_q.models import Task
import os
from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Publication
from friendship.models import Follow
from cities_light.models import Country


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
