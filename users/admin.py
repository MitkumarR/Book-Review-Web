from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name', 'join_date', 'country', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'name')
    list_filter = ('is_active', 'is_staff', 'join_date')
