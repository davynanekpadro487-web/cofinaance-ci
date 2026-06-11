from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('Informations Cofinance', {
            'fields': ('role', 'telephone', 'region', 'date_naissance', 'photo_profil', 'is_online')
        }),
    )
    list_display = ['username', 'email', 'role', 'telephone', 'is_online', 'is_staff']
    list_filter = ['role', 'is_online', 'is_staff', 'is_superuser', 'is_active']

admin.site.register(User, CustomUserAdmin)
