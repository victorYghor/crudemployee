from rest_framework import serializers

from employee.models import Employee


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "email", "name", "last_name", "is_superuser", "department"]

