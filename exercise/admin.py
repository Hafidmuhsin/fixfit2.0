from django.contrib import admin
from .models import ExerciseLog

@admin.register(ExerciseLog)
class ExerciseLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_name', 'duration_minutes', 'calories_burned', 'intensity', 'created_at')
    list_filter = ('intensity', 'created_at')
