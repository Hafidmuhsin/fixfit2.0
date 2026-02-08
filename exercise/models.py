from django.db import models
from django.conf import settings

class ExerciseType(models.Model):
    name = models.CharField(max_length=100)
    calories_per_hour = models.IntegerField(help_text="Burn rate per hour (kcal)")
    intensity_default = models.CharField(max_length=20, default='Medium')

    def __str__(self):
        return self.name

class ExerciseLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise_type = models.ForeignKey(ExerciseType, on_delete=models.SET_NULL, null=True, blank=True)
    activity_name = models.CharField(max_length=100, blank=True) # Fallback / Custom name
    duration_minutes = models.IntegerField()
    calories_burned = models.IntegerField(help_text="Calculated calories burned")
    intensity = models.CharField(max_length=10, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Medium')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Auto-calculate calories if type is provided and calories not manually set
        if self.exercise_type and not self.calories_burned:
            # Simple formula: (Duration / 60) * Cal/Hr
            self.calories_burned = int((self.duration_minutes / 60) * self.exercise_type.calories_per_hour)
            if not self.activity_name:
                self.activity_name = self.exercise_type.name
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.activity_name}"
