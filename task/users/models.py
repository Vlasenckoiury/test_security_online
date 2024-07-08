from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Заказчик'),
        ('employee', 'Сотрудник'),
        ('admin', 'Admin'),
    )

    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    photo = models.ImageField(upload_to='users/photos/', null=False, blank=False)

    def __str__(self):
        return self.username


class Task(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Ожидает исполнителя'),
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнена'),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tasks')
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    report = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.closed_at:
            self.closed_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
