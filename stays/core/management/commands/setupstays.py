from django.core.management import call_command, CommandError
from django.core.management.base import BaseCommand
import os
from django.contrib.auth import get_user_model
from model_bakery import baker
from friendship.models import Follow
from core.models import Publication, ContentTypes
from cities_light.models import Country
from datetime import datetime
from uuid import uuid4
import random
from io import StringIO


class Command(BaseCommand):
    help = 'Setup'

    def run_command_and_get_output(self, command):
        out = StringIO()
        call_command(command, stdout=out)
        return out.getvalue().strip()

    def handle(self, *args, **options):
        try:
            # Run makemigrations and capture output
            makemigrations_output = self.run_command_and_get_output('makemigrations')

            # Run migrate and capture output
            migrate_output = self.run_command_and_get_output('migrate')

            # Check if migrations were necessary
            if ('No changes detected' in makemigrations_output and
                'No migrations to apply' in migrate_output):
                self.stdout.write('No migrations necessary.')
            elif 'Migrations for' in makemigrations_output and 'Applying' in migrate_output:
                self.stdout.write('Migrations applied successfully.')
            else: 
                raise CommandError(f'{makemigrations_output}\n{migrate_output}')

        except CommandError as e:
            self.stdout.write(f'Error applying migrations: {str(e)}')
            return

        if os.getenv('RUNNING_FROM_TEST'):
            # Create a Country instance for Italy
            Country.objects.create(name='Italy', code2='IT')

        elif Country.objects.all().exists():
            try:
                france = Country.objects.filter(name='France', code2='FR')
                if france.exists():
                    self.stdout.write("Cities light country already exists with France")
                else:
                    Country.objects.create(name='France', code2='FR')
            except Exception as e:
                self.stdout.write(f'Error in model or database Cities light Country: {str(e)}')
        else:
            try:
                # Run cities_light command
                call_command('cities_light')
            except Exception as e:
                print(f'Error running cities_light command: {str(e)}')

        User = get_user_model()
        words = [
            'Full', 'Story', 'Test', 'Publication', 'Voice', 'Audio', 'Home', 'View'
            'apple', 'banana', 'cherry', 'date', 'elderberry',
            'fig', 'grape', 'honeydew', 'iceberg', 'jackfruit',
            'kiwi', 'lemon', 'mango', 'nectarine', 'orange',
            'pineapple', 'quince', 'raspberry', 'strawberry', 'tangerine',
            'ugli', 'vanilla', 'watermelon', 'xigua', 'yellow'
        ]
        country = Country.objects.first()  # or get the country you want

        # Create 3 profiles
        profiles = []
        for i in range(3):
            profile = baker.make(User,
                email=f'testadmin{i}@example.com',
                slug=f"testadmin{i}",
                username=f'testadmin{i}',
                profile_picture='picture.jpg'
            )
            profile.set_password('testpassword')
            profile.save()
            profiles.append(profile)

            # Create 4 publications per profile
            for _ in range(4):
                Publication.objects.create(
                    uuid=uuid4(),
                    title=' '.join(random.choices(words, k=3)),
                    author_username=profile.username,
                    author_slug=profile.slug,
                    picture='',
                    text_story='This is a full story.',
                    content_type=ContentTypes.text.value[0],
                    season_of_stay='Winter',
                    year_of_stay=2000,
                    summary='This is a summary.',
                    created_at=datetime.now(),
                    country_code_of_stay=country.code2,
                    published_from_country_code="FR",
                    upvotes_count=0
                )
        
        # Create 1 superuser
        superadmin = baker.make(
            User,
            email='superadmin@stays.com',
            slug=f"superadmin{uuid4()}",
            username='superadmin',
            is_superuser=True,
            is_staff=True
        )
        superadmin.set_password('testpassword')
        superadmin.save()

        profiles.append(superadmin)
        # Make each profile follow the others
        for profile in profiles:
            for other_profile in profiles:
                if profile != other_profile:
                    Follow.objects.add_follower(follower=profile, followee=other_profile)
