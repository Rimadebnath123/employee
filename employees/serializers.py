from rest_framework import serializers
from .models import Employee
from django.contrib.auth.models import User

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'department', 'role', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username', 'email', 'password']

    def create(self, validated_data):
        user=User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
        )
        return user

class LoginSerializer(serializers.Serializer):
   username=serializers.CharField(required=True)
   password=serializers.CharField(required=True,write_only=True)
#if we want we use email alternate of password
