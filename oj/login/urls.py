from django.urls import path
from .views import login,initial,register,save_user

urlpatterns = [ path('',initial),
path('login/',login),
path('registration/',register),
path('saveUser/',save_user),]