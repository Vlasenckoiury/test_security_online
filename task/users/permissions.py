from rest_framework import permissions


class IsCustomerOrAssignedEmployee(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.user_type == 'admin':
            return True
        return obj.customer == request.user or obj.employee == request.user


class IsCustomer(permissions.BasePermission):  # Разрешает только заказчикам
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'customer'
