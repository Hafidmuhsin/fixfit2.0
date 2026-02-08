from django.core.management.base import BaseCommand
from exercise.models import ExerciseType

class Command(BaseCommand):
    help = 'Seeds database with common exercise types'

    def handle(self, *args, **kwargs):
        items = [
            {'name': 'Walking (Normal)', 'calories_per_hour': 250},
            {'name': 'Running (5 mph)', 'calories_per_hour': 600},
            {'name': 'Running (8 mph)', 'calories_per_hour': 900},
            
            {'name': 'Cycling (Moderate)', 'calories_per_hour': 500},
            {'name': 'Swimming (Freestyle)', 'calories_per_hour': 600},
            
            {'name': 'HIIT / Circuit', 'calories_per_hour': 700},
            {'name': 'Weight Lifting (Heavy)', 'calories_per_hour': 300},
            {'name': 'Yoga', 'calories_per_hour': 200},
            {'name': 'Basketball', 'calories_per_hour': 500},
            {'name': 'Soccer', 'calories_per_hour': 600},
        ]
        
        for item in items:
            ExerciseType.objects.get_or_create(name=item['name'], defaults=item)
            
        self.stdout.write(self.style.SUCCESS("Exercise Types seeded"))
