from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Task


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'full_name', 'email', 'phone', 'user_type']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('full_name', 'email', 'phone', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'employee', 'title', 'status', 'created_at', 'updated_at', 'closed_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'created_at', 'updated_at', 'closed_at')


