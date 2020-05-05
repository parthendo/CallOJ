from django.urls import path
from .views import loginView,logoutView,initialView,registerView,saveUserView

urlpatterns = [ path('',initialView),
path('login/',loginView),
path('registration/',registerView),
path('saveUser/',saveUserView),
path('logout/',logoutView),]