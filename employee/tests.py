from unittest import TestCase

from django.test import RequestFactory
from rest_framework.test import force_authenticate
import json

class TestAuth(TestCase):
    def setUp(self):
        pass