import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fixfit.settings')
django.setup()

from nutrition.models import FoodItem

# List of foods with their nutritional values (Name, Calories, Protein, Carbs, Fats)
foods = [
    # Fruits
    {"name": "Apple (Medium)", "calories": 95, "protein": 0.5, "carbs": 25, "fats": 0.3},
    {"name": "Banana (Medium)", "calories": 105, "protein": 1.3, "carbs": 27, "fats": 0.4},
    {"name": "Orange (Medium)", "calories": 62, "protein": 1.2, "carbs": 15.4, "fats": 0.2},
    {"name": "Strawberries (1 cup)", "calories": 53, "protein": 1.1, "carbs": 12.7, "fats": 0.5},
    {"name": "Blueberries (1 cup)", "calories": 84, "protein": 1.1, "carbs": 21.4, "fats": 0.5},
    {"name": "Avocado (Half)", "calories": 160, "protein": 2, "carbs": 8.5, "fats": 14.7},

    # Vegetables
    {"name": "Broccoli (1 cup)", "calories": 55, "protein": 3.7, "carbs": 11.2, "fats": 0.6},
    {"name": "Spinach (1 cup)", "calories": 7, "protein": 0.9, "carbs": 1.1, "fats": 0.1},
    {"name": "Carrot (Medium)", "calories": 25, "protein": 0.6, "carbs": 5.8, "fats": 0.1},
    {"name": "Sweet Potato (Medium)", "calories": 103, "protein": 2.3, "carbs": 23.6, "fats": 0.2},

    # Grains & Carbs
    {"name": "Brown Rice (1 cup cooked)", "calories": 216, "protein": 5, "carbs": 44.8, "fats": 1.8},
    {"name": "White Rice (1 cup cooked)", "calories": 205, "protein": 4.2, "carbs": 44.5, "fats": 0.4},
    {"name": "Oatmeal (1 cup cooked)", "calories": 158, "protein": 6, "carbs": 27, "fats": 3.2},
    {"name": "Whole Wheat Bread (1 slice)", "calories": 81, "protein": 4, "carbs": 13.7, "fats": 1.1},
    {"name": "Quinoa (1 cup cooked)", "calories": 222, "protein": 8.1, "carbs": 39.4, "fats": 3.6},

    # Proteins
    {"name": "Chicken Breast (100g)", "calories": 165, "protein": 31, "carbs": 0, "fats": 3.6},
    {"name": "Salmon (100g)", "calories": 206, "protein": 22, "carbs": 0, "fats": 13},
    {"name": "Egg (Large)", "calories": 78, "protein": 6.3, "carbs": 0.6, "fats": 5.3},
    {"name": "Tofu (100g)", "calories": 76, "protein": 8, "carbs": 1.9, "fats": 4.8},
    {"name": "Greek Yogurt (1 cup)", "calories": 100, "protein": 17, "carbs": 6, "fats": 0.7},
    {"name": "Almonds (1 oz)", "calories": 164, "protein": 6, "carbs": 6.1, "fats": 14.2},
    {"name": "Peanut Butter (2 tbsp)", "calories": 188, "protein": 8, "carbs": 6.3, "fats": 16.1},

    # Dairy & Alternatives
    {"name": "Milk (1 cup)", "calories": 103, "protein": 8, "carbs": 12, "fats": 2.4},
    {"name": "Almond Milk (1 cup)", "calories": 30, "protein": 1, "carbs": 1, "fats": 2.5},
    {"name": "Cheddar Cheese (1 oz)", "calories": 115, "protein": 7, "carbs": 0.6, "fats": 9.4},

    # Common Meals
    {"name": "Pizza Slice", "calories": 285, "protein": 12, "carbs": 36, "fats": 10},
    {"name": "Burger (Cheeseburger)", "calories": 303, "protein": 15, "carbs": 30, "fats": 14},
    {"name": "Salad (Caesar)", "calories": 184, "protein": 5, "carbs": 8, "fats": 15},
    {"name": "Pasta with Sauce (1 cup)", "calories": 300, "protein": 10, "carbs": 50, "fats": 6},
]

print(f"Starting to populate {len(foods)} food items...")

count = 0
for food_data in foods:
    food, created = FoodItem.objects.get_or_create(
        name=food_data['name'],
        defaults={
            'calories': food_data['calories'],
            'protein': food_data['protein'],
            'carbs': food_data['carbs'],
            'fats': food_data['fats']
        }
    )
    if created:
        print(f"Added: {food.name}")
        count += 1
    else:
        # Update existing items just in case values changed
        food.calories = food_data['calories']
        food.protein = food_data['protein']
        food.carbs = food_data['carbs']
        food.fats = food_data['fats']
        food.save()
        print(f"Updated: {food.name}")

print(f"\nSuccessfully processed database. Added {count} new items.")
