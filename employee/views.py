from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Employee, Department
from .serializers import EmployeeSerializer, EmployeeCreateSerializer


class EmployeeViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        List employees.
        """
        user = request.user

        if user.is_superuser:
            employees = Employee.objects.all()
        elif user.is_manager:
            employees = Employee.objects.filter(department=user.department)
        else:
            raise PermissionDenied("You are not authorized to view employee profiles.")

        search_param = request.query_params.get("search", None)
        if search_param:
            employees = employees.filter(
                first_name__icontains=search_param
            ) | employees.filter(
                last_name__icontains=search_param
            ) | employees.filter(
                email__icontains=search_param
            ) | employees.filter(
                department__name__contains=search_param
            )

        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Get a specific employee.
        """
        user = request.user
        employee_id = kwargs.get("pk")
        employee = get_object_or_404(Employee, id=employee_id)

        if user.is_superuser or (user.is_manager and employee.department == user.department):
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise PermissionDenied("You are not authorized to view this employee.")

    def create(self, request):
        """
        Create a new employee.
        """
        user = request.user
        if not (user.is_superuser or user.is_manager):
            raise PermissionDenied("You are not authorized to create an employee.")

        data = request.data
        serializer = EmployeeCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        if user.is_manager and serializer.validated_data.get("department") != user.department:
            raise PermissionDenied("Managers can only create employees in their own department.")


        employee = serializer.save()
        return Response(EmployeeSerializer(employee).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Update an existing employee.
        """
        user = request.user
        employee_id = kwargs.get("pk")
        employee = get_object_or_404(Employee, id=employee_id)

        if not (user.is_superuser or (user.is_manager and employee.department == user.department)):
            raise PermissionDenied("You are not authorized to update this employee.")
        data = request.data
        serializer = EmployeeCreateSerializer(employee, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(EmployeeSerializer(employee).data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an employee.
        """
        user = request.user
        employee_id = kwargs.get("pk")
        employee = get_object_or_404(Employee, id=employee_id)

        if not (user.is_superuser or (user.is_manager and employee.department == user.department)):
            raise PermissionDenied("You are not authorized to delete this employee.")

        employee.delete()
        return Response({"detail": "Employee deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


