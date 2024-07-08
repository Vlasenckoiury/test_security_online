from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser, Task

User = get_user_model()


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


# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password', 'photo']
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'photo': {'required': True}
#         }

    # def create(self, validated_data):
    #     user = CustomUser.objects.create_user(**validated_data)
    #     return user


class TaskSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.username')
    employee = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Task
        fields = ['id', 'customer', 'employee', 'title', 'description', 'status', 'created_at', 'updated_at', 'closed_at', 'report']
        read_only_fields = ['id', 'customer', 'created_at', 'updated_at', 'closed_at', 'employee']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'email', 'phone']
