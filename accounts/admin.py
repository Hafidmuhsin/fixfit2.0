from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'username', 'is_staff', 'is_active', 'is_premium', 'date_joined']
    list_filter = ['is_staff', 'is_active', 'is_premium']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'gender', 'height', 'weight', 'profile_picture', 'bio', 'is_premium', 'dark_mode')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'gender', 'height', 'weight', 'profile_picture', 'bio', 'is_premium', 'dark_mode')}),
    )
    ordering = ['email']

admin.site.register(User, CustomUserAdmin)
