from django.test import SimpleTestCase
from django.urls import reverse, resolve
from login.views import loginView,logoutView,initialView,registerView,saveUserView
class TestUrls(SimpleTestCase):
    def test_inital_url_is_resolved(self):
        url = reverse('initialUrl')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,initialView)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,loginView)

    def test_register_url_is_resolved(self):
        url = reverse('register')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,registerView)

    def test_saveUser_url_is_resolved(self):
        url = reverse('saveUser')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,saveUserView)
    
    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,logoutView)