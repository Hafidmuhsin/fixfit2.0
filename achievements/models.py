from django.db import models
from django.conf import settings

class UserGoal(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='goal')
    daily_calories = models.IntegerField(default=2500, help_text="Target daily calorie intake")
    daily_water_ml = models.IntegerField(default=2500, help_text="Target daily water in ml")
    daily_sleep_hours = models.DecimalField(max_digits=4, decimal_places=1, default=8.0, help_text="Target hours of sleep")
    daily_exercise_minutes = models.IntegerField(default=45, help_text="Target active minutes per day")
    target_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Target weight in kg")

    # Planning Fields
    GOAL_CHOICES = [
        ('lose_weight', 'Lose Weight'),
        ('maintain', 'Maintain Weight'),
        ('gain_muscle', 'Gain Muscle'),
    ]
    primary_goal = models.CharField(max_length=20, choices=GOAL_CHOICES, default='maintain')
    
    ACTIVITY_CHOICES = [
        ('sedentary', 'Sedentary (Office Job)'),
        ('lightly_active', 'Lightly Active (1-3 days/week)'),
        ('moderately_active', 'Moderately Active (3-5 days/week)'),
        ('very_active', 'Very Active (6-7 days/week)'),
    ]
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, default='moderately_active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Goals for {self.user.username}"
