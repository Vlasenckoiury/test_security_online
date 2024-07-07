from rest_framework_simplejwt.views import TokenObtainPairView
from . import models
from .serializers import CustomTokenObtainPairSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Task
from .serializers import TaskSerializer
from rest_framework.exceptions import PermissionDenied


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'customer'


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_permissions(self):
    #     if self.action == 'create':
    #         self.permission_classes = [IsCustomer]
    #     return super(TaskViewSet, self).get_permissions()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return Task.objects.all()
        elif user.user_type == 'employee':
            return Task.objects.filter(models.Q(employee=user) | models.Q(customer=user))
        elif user.user_type == 'customer':
            return Task.objects.filter(customer=user)
        else:
            return Task.objects.filter(customer=user)

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type != 'customer':
            raise PermissionDenied("Только заказчики могут создавать задачи.")
        serializer.save(customer=user)

    def create(self, request, *args, **kwargs):
        if request.user.user_type != 'customer':
            return Response({'detail': 'Только заказчики могут создавать задачи.'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    # def perform_create(self, serializer):
    #     serializer.save(customer=self.request.user)

    def get_permissions(self):
        if self.action in ['create']:
            return [IsCustomer()]
        return [permissions.IsAuthenticated()]