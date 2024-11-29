import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.exceptions import ValidationError


class Department(models.Model):
    name=models.CharField(max_length=100, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = "department"

class Employee(AbstractUser):
    username = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    is_superuser = models.BooleanField(null=False, blank=False, default=False)
    is_manager = models.BooleanField(null=False, blank=False, default=False)
    email = models.CharField(max_length=255, null=False, blank=False, unique=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        related_name="employees",
        null=True,
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    class Meta:
        unique_together = (("username", "last_name", "email"),)
        db_table = "employee"
