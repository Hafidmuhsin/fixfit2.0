from django.db import models
from django.conf import settings

class FoodItem(models.Model):
    name = models.CharField(max_length=200)
    calories = models.IntegerField(help_text="Calories per serving")
    protein = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    carbs = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    fats = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    
    def __str__(self):
        return self.name

class CalorieLog(models.Model):
    MEAL_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True, blank=True)
    food_name = models.CharField(max_length=200) # For custom entries
    calories = models.IntegerField()
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES, default='Snack')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.food_name} ({self.calories} kcal)"
