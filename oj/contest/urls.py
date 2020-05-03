from django.urls import path, include
from .views import contestsView
urlpatterns = [
    path('',contestsView),
]