from django.urls import path
from django.conf.urls import url
from .views import loginView,logoutView,initialView,registerView,saveUserView,activate

urlpatterns = [ path('',initialView,name='initialUrl'),
path('login/',loginView,name='login'),
path('registration/',registerView,name='register'),
path('saveUser/',saveUserView,name='saveUser'),
path('logout/',logoutView,name='logout'),
url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate, name='activate'),]