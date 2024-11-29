from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, views
from rest_framework.decorators import action
from rest_framework.response import Response

from employee.models import Employee
from employee.serializers import UserSerializer


class EmployeeViewSet(viewsets.ViewSet):
    def retrive(self):
        return JsonResponse(data="works", status=200)

class AuthViewSet(views.APIView):
    @action(detail=False, methods=["post"], url_name="set-password", url_path="set_password")
    def set_password(self, request):
        """
        Permite definir ou redefinir a senha do usuário usando o token de email, para quando o usuário esquecer
        a senha ou quando for o seu primeiro acesso.
        """
        email_token = request.data.get("email_token")
        password = request.data.get("password")

        if not email_token or not password:
            return Response({"error": "email_token and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(Employee, email_token=email_token)
        user.set_password(password)
        # Faz que não seja mais possível usar aquele token depois de ter modificado a senha.
        user.email_token = None
        user.save()
        return Response({"message": "Password set successfully."}, status=status.HTTP_200_OK)

    def get(self, request):
        return Response(status=200)

    def post(self, request):
        """
        Autentica o usuário e retorna um token JWT.
        """
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(Employee, email=email)
        if not user.check_password(password):
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        token = user.generate_jwt_token()
        res = UserSerializer(user).data | {"token": token}
        return Response(res, status=status.HTTP_200_OK)
