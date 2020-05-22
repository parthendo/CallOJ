from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
import json

class TestViews(TestCase):
    def test_inital(self):
        client = Client()
        response = client.get(reverse('initialUrl'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')

    def test_login(self):
        client = Client()
        response = self.client.post(reverse('login'),data={'username':'anonymous','pass':'123'})
        self.assertEquals(response.status_code,302)

    def test_register(self):
        client = Client()
        response = client.get(reverse('register'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'registration.html')

    def test_logout(self):
        client = Client()
        response = client.get(reverse('logout'))
        self.assertEquals(response.status_code,302)

    def test_saveUser(self):
        client = Client()

