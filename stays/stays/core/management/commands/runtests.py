import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Run pytest on specific apps'

    def handle(self, *args, **options):
        apps = ['core', 'users', 'locations', 'stays']
        for app in apps:
            self.stdout.write(f'Running tests for {app}...')
            subprocess.run(['pytest', f'{app}/tests/test_*.py', '-s', '-v'])