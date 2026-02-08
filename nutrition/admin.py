from django.contrib import admin
from .models import FoodItem, CalorieLog

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'protein', 'carbs', 'fats')
    search_fields = ('name',)

@admin.register(CalorieLog)
class CalorieLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'food_name', 'calories', 'meal_type', 'created_at')
    list_filter = ('meal_type', 'created_at')
