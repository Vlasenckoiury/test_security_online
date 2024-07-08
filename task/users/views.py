from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, EmployeeSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import *
from .serializers import TaskSerializer
from rest_framework.exceptions import PermissionDenied
from .permissions import IsCustomerOrReadOnly, IsCustomer, IsEmployee, IsCustomerOrEmployee
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


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsCustomerOrEmployee]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'customer':
            return self.queryset.filter(customer=user)
        elif user.user_type == 'employee':
            return self.queryset
        return self.queryset.none()

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @action(detail=True, methods=['patch'], permission_classes=[IsEmployee])
    def assign(self, request, pk=None):
        task = self.get_object()
        if task.employee is not None:
            return Response({'error': 'Задача уже назначена другому сотруднику.'}, status=status.HTTP_400_BAD_REQUEST)
        task.employee = request.user
        task.status = 'in_progress'
        task.save()
        return Response({'status': 'Задача назначена'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], permission_classes=[IsEmployee])
    def close(self, request, pk=None):
        task = self.get_object()
        if task.employee != request.user:
            return Response({'error': 'Только назначенный сотрудник может закрыть задачу.'}, status=status.HTTP_403_FORBIDDEN)
        if task.status == 'done':
            return Response({'error': 'Задача уже закрыта.'}, status=status.HTTP_400_BAD_REQUEST)
        task.status = 'done'
        task.closed_at = timezone.now()
        task.report = request.data.get('report', '')
        if not task.report:
            return Response({'error': 'Отчет не может быть пустым при закрытии задачи.'}, status=status.HTTP_400_BAD_REQUEST)
        task.save()
        return Response({'status': 'Задача закрыта'}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'customer':
            return self.queryset.filter(user_type='employee')
        return self.queryset.none()
