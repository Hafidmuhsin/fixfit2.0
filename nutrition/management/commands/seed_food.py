from django.core.management.base import BaseCommand
from nutrition.models import FoodItem

class Command(BaseCommand):
    help = 'Seeds database with common food items'

    def handle(self, *args, **kwargs):
        items = [
            # Fruits
            {'name': 'Apple (Medium)', 'calories': 95, 'protein': 0.5, 'carbs': 25, 'fats': 0.3},
            {'name': 'Banana (Medium)', 'calories': 105, 'protein': 1.3, 'carbs': 27, 'fats': 0.4},
            {'name': 'Orange', 'calories': 62, 'protein': 1.2, 'carbs': 15, 'fats': 0.2},
            
            # Meals
            {'name': 'Oatmeal (1 cup)', 'calories': 150, 'protein': 5, 'carbs': 27, 'fats': 3},
            {'name': 'Chicken Breast (Grilled, 100g)', 'calories': 165, 'protein': 31, 'carbs': 0, 'fats': 3.6},
            {'name': 'Salmon (Grilled, 100g)', 'calories': 208, 'protein': 20, 'carbs': 0, 'fats': 13},
            {'name': 'Brown Rice (1 cup)', 'calories': 216, 'protein': 5, 'carbs': 45, 'fats': 1.8},
            {'name': 'Pizza Slice (Pepperoni)', 'calories': 285, 'protein': 12, 'carbs': 36, 'fats': 10},
            {'name': 'Burger (Cheeseburger)', 'calories': 303, 'protein': 15, 'carbs': 30, 'fats': 14},
            
            # Snacks
            {'name': 'Almonds (1 oz)', 'calories': 164, 'protein': 6, 'carbs': 6, 'fats': 14},
            {'name': 'Greek Yogurt (1 cup)', 'calories': 100, 'protein': 10, 'carbs': 8, 'fats': 0},
            
            # Drinks
            {'name': 'Coffee (Black)', 'calories': 2, 'protein': 0, 'carbs': 0, 'fats': 0},
            {'name': 'Orange Juice (1 cup)', 'calories': 112, 'protein': 2, 'carbs': 26, 'fats': 0.5},
        ]
        
        for item in items:
            obj, created = FoodItem.objects.get_or_create(name=item['name'], defaults=item)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created food: {obj.name}'))
            else:
                self.stdout.write(f'Skipped: {obj.name}')
