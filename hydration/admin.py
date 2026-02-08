from django.contrib import admin
from .models import WaterIntake

@admin.register(WaterIntake)
class WaterIntakeAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount_ml', 'created_at')
    list_filter = ('created_at',)
