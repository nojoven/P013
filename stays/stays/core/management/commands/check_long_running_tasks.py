from django.core.management.base import BaseCommand
from django_q.models import OrmQ
from datetime import datetime

class Command(BaseCommand):
    help = 'Check for long running tasks in Django Q'

    def handle(self, *args, **options):
        # Get all tasks
        all_tasks = OrmQ.objects.all()

        # Filter tasks that are running for more than 30 minutes
        long_running_tasks = [task for task in all_tasks if task.stopped and task.started and (task.stopped - task.started).total_seconds() > 1800]

        # Print long running tasks
        for task in long_running_tasks:
            time_taken = (task.stopped - task.started).total_seconds()
            self.stdout.write(f'Task ID: {task.id}, Start Time: {task.started}, Time Taken: {time_taken} seconds')