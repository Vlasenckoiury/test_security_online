# tasks/permissions.py
from rest_framework import permissions


class IsCustomerOrReadOnly(permissions.BasePermission):
    """
    Проверяет, является ли пользователь заказчиком для создания задачи или сотрудником для просмотра задач.
    """
    def has_permission(self, request, view):
        user = request.user
        if view.action in ['create']:
            return user.user_type == 'customer'
        if view.action in ['list', 'retrieve', 'update', 'partial_update']:
            return user.user_type in ['customer', 'employee']
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.user_type == 'customer':
            return obj.customer == user
        elif user.user_type == 'employee':
            return obj.employee is None or obj.employee == user or user.has_perm('tasks.view_all_tasks')
        return False


# class IsCustomer(permissions.BasePermission):
#     """
#     Разрешение на доступ только для пользователей с ролью 'customer'.
#     """
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.user_type == 'customer'


class IsCustomerOrEmployee(permissions.BasePermission):
    """
    Разрешение для заказчиков и сотрудников.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.user_type == 'customer' or request.user.user_type == 'employee')


class IsCustomer(permissions.BasePermission):
    """
    Разрешение для заказчиков.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'customer'


class IsEmployee(permissions.BasePermission):
    """
    Разрешение для сотрудников.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'employee'

