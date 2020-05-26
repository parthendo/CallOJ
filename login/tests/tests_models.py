from django.test import TestCase
from django.contrib.auth.models import User
class TestModels(TestCase):
    def test_User(self):
        user = User.objects.create_user(username="anonymous",first_name="ano",last_name="nymous",email="test@gmail.com",password="123")
        createdUser = User.objects.get(username="anonymous")

