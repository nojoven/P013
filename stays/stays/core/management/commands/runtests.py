import os
import fnmatch
import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Run pytest on specific apps'

    def handle(self, *args, **options):
        apps = ['core', 'users', 'locations', 'stays']
        for app in apps:
            self.stdout.write(f'Running tests for {app}...')
            for dirpath, dirnames, filenames in os.walk(f'{app}/tests'):
                for filename in fnmatch.filter(filenames, 'test_*.py'):
                    test_file = os.path.join(dirpath, filename)
                    self.stdout.write(f'Running tests in {test_file}...')
                    subprocess.run(['pytest', '--cov=.', '--cov-append', test_file, '-s', '-v'])