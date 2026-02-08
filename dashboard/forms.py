from django import forms
from nutrition.models import CalorieLog, FoodItem
from hydration.models import WaterIntake
from exercise.models import ExerciseLog, ExerciseType
from sleep.models import SleepLog
from achievements.models import UserGoal
from accounts.models import User

class FoodLogForm(forms.ModelForm):
    food_item = forms.ModelChoiceField(queryset=FoodItem.objects.all(), required=False, empty_label="Select Food (Optional)")
    
    class Meta:
        model = CalorieLog
        fields = ['food_item', 'food_name', 'calories', 'meal_type']
        widgets = {
            'food_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Custom Food Name'}),
            'calories': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Calories'}),
            'meal_type': forms.Select(attrs={'class': 'form-select'}),
        }

class WaterLogForm(forms.ModelForm):
    class Meta:
        model = WaterIntake
        fields = ['amount_ml']

class ExerciseLogForm(forms.ModelForm):
    exercise_type = forms.ModelChoiceField(queryset=ExerciseType.objects.all(), required=False, empty_label="Select Type")
    
    class Meta:
        model = ExerciseLog
        fields = ['exercise_type', 'activity_name', 'duration_minutes', 'intensity']

class SleepLogForm(forms.ModelForm):
    class Meta:
        model = SleepLog
        fields = ['duration_minutes', 'quality', 'notes']

class GoalForm(forms.ModelForm):
    class Meta:
        model = UserGoal
        fields = ['daily_calories', 'daily_water_ml', 'daily_sleep_hours', 'daily_exercise_minutes', 'target_weight', 'primary_goal', 'activity_level']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'height', 'weight']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

# Targeted forms for the analysis page to avoid validation errors on missing fields
class ProfileAnalysisForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['gender', 'date_of_birth', 'height', 'weight']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class GoalAnalysisForm(forms.ModelForm):
    class Meta:
        model = UserGoal
        fields = ['primary_goal', 'activity_level']
