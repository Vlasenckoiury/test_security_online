from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser, Task


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        user = CustomUser.objects.get(username=self.user.username)
        data.update({
            'user': {
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'phone': user.phone,
                'user_type': user.user_type,
            }
        })
        return data


# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = '__all__'
#
#     def validate(self, data):
#         if data.get('status') == 'completed' and not data.get('report'):
#             raise serializers.ValidationError("Отчет не может быть пустым при закрытии задачи.")
#         return data

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'customer', 'employee', 'title', 'description', 'status', 'created_at', 'updated_at', 'closed_at', 'report']
        read_only_fields = ['id', 'customer', 'created_at', 'updated_at', 'closed_at', 'status']

    def validate(self, data):
        if self.instance and self.instance.status == 'completed' and data.get('status') != 'completed':
            raise serializers.ValidationError("Задача выполнена и не может быть отредактирована.")
        if data.get('status') == 'completed' and not data.get('report'):
            raise serializers.ValidationError("Отчет не может быть пустым при закрытии задачи.")
        return data
