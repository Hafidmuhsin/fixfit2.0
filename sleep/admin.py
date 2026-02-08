from django.contrib import admin
from .models import SleepLog

@admin.register(SleepLog)
class SleepLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'duration_minutes', 'quality', 'created_at')
    list_filter = ('quality', 'created_at')
