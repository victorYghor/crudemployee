from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from employee.models import Employee, Department


class EmployeeSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(
        queryset=Department.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = Employee
        fields = ["id", "email", "first_name", "last_name", "is_manager" , "is_superuser", "department"]

class EmployeeCreateSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(
        queryset=Department.objects.all(),
        slug_field="name"
    )

    # Validação do primeiro nome
    def validate_first_name(self, value):
        if not value or value.strip() == "":
            raise ValidationError("O primeiro nome não pode estar vazio.")
        return value

    # Validação do último nome
    def validate_last_name(self, value):
        if not value or value.strip() == "":
            raise ValidationError("O último nome não pode estar vazio.")
        return value

    # Validação global para garantir que um gerente tenha um departamento
    def validate(self, data):
        if data.get("is_manager") and not data.get("department"):
            raise ValidationError("Um gerente deve estar associado a um departamento.")
        return data

    class Meta:
        model = Employee
        fields = ["email", "first_name", "last_name", "department", "is_manager"]