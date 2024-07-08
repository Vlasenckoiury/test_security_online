from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, EmployeeSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import *
from .serializers import TaskSerializer
from rest_framework.exceptions import PermissionDenied
from .permissions import IsCustomerOrReadOnly, IsCustomer
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'customer':
            return Task.objects.filter(customer=user)
        elif user.user_type == 'employee':
            return Task.objects.all()
        return Task.objects.none()

    def perform_create(self, serializers):
        user = self.request.user
        if user.user_type == 'customer':
            serializers.save(customer=user)
        else:
            raise PermissionDenied("Только заказчики могут создавать задачи.")


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(user_type='employee')
    serializer_class = EmployeeSerializer
    permission_classes = [IsCustomer]

    def get_permissions(self):  # Применяем пользовательское разрешение.
        return [permission() for permission in self.permission_classes]
