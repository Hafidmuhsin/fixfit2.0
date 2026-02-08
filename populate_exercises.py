
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fixfit.settings')
django.setup()

from exercise.models import ExerciseType

# List of exercises with calories burned per hour (approximate for average person)
exercises = [
    {"name": "Running (Moderate Pace)", "calories_per_hour": 600, "intensity_default": "Medium"},
    {"name": "Running (Fast Pace)", "calories_per_hour": 850, "intensity_default": "High"},
    {"name": "Walking (Brisk)", "calories_per_hour": 300, "intensity_default": "Low"},
    {"name": "Cycling (Moderate)", "calories_per_hour": 500, "intensity_default": "Medium"},
    {"name": "Cycling (Intense)", "calories_per_hour": 700, "intensity_default": "High"},
    {"name": "Swimming (Laps)", "calories_per_hour": 500, "intensity_default": "Medium"},
    {"name": "Weightlifting (General)", "calories_per_hour": 300, "intensity_default": "Medium"},
    {"name": "Yoga (Hatha)", "calories_per_hour": 200, "intensity_default": "Low"},
    {"name": "HIIT (High Intensity Interval Training)", "calories_per_hour": 700, "intensity_default": "High"},
    {"name": "Jump Rope", "calories_per_hour": 800, "intensity_default": "High"},
    {"name": "Hiking", "calories_per_hour": 400, "intensity_default": "Medium"},
    {"name": "Dancing (Zumba/Aerobic)", "calories_per_hour": 450, "intensity_default": "Medium"},
    {"name": "Elliptical Machine", "calories_per_hour": 550, "intensity_default": "Medium"},
    {"name": "Rowing (Moderate)", "calories_per_hour": 600, "intensity_default": "High"},
    {"name": "Basketball (Game)", "calories_per_hour": 720, "intensity_default": "High"},
    {"name": "Soccer (Competitive)", "calories_per_hour": 750, "intensity_default": "High"},
    {"name": "Tennis (Singles)", "calories_per_hour": 500, "intensity_default": "Medium"},
    {"name": "Boxing (Sparring)", "calories_per_hour": 800, "intensity_default": "High"},
    {"name": "Pilates", "calories_per_hour": 250, "intensity_default": "Low"},
]

print(f"Starting to populate {len(exercises)} exercise types...")

count = 0
for ex_data in exercises:
    ex_type, created = ExerciseType.objects.get_or_create(
        name=ex_data['name'],
        defaults={
            'calories_per_hour': ex_data['calories_per_hour'],
            'intensity_default': ex_data['intensity_default']
        }
    )
    if created:
        print(f"Added: {ex_type.name}")
        count += 1
    else:
        # Update existing items
        ex_type.calories_per_hour = ex_data['calories_per_hour']
        ex_type.intensity_default = ex_data['intensity_default']
        ex_type.save()
        print(f"Updated: {ex_type.name}")

print(f"\nSuccessfully processed database. Added {count} new exercise types.")
