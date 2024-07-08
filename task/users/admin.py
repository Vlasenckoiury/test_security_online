from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, Task


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'full_name', 'email', 'phone', 'user_type', 'photo_thumbnail']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('full_name', 'email', 'phone', 'user_type', 'photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 50%;" />', obj.photo.url)
        return "No photo"
    photo_thumbnail.short_description = 'Фото'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'employee', 'title', 'status', 'created_at', 'updated_at', 'closed_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'created_at', 'updated_at', 'closed_at')


