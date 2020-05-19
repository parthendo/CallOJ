from django.urls import path
from .views import profileView,updateProfileView,changesToProfileView

urlpatterns = [ path('',profileView),
path('updateProfile/',updateProfileView),
path('changesToProfile/',changesToProfileView),
]