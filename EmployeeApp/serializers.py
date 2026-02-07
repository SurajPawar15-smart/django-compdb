from rest_framework import serializers
from .models import Department, Employee

from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()

from rest_framework import serializers
from .models import Department, Employee

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

# class DepartmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Department
#         fields = [
#             'department_id',
#             'department_name',
#             'description',
#             'created_at',
#         ]
# class EmployeeSerializer(serializers.ModelSerializer):
#     department_name = serializers.CharField(
#         source='department.department_name',
#         read_only=True
#     )

#     class Meta:
#         model = Employee
#         fields = [
#             'employee_id',
#             'employee_name',
#             'email',
#             'phone',
#             'designation',
#             'salary',
#             'date_of_joining',
#             'department',
#             'department_name',
#             'photo',
#             'is_active',
#             'created_at',
#             'updated_at',
#         ]
