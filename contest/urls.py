from django.urls import path, include
from .views import contestsView,createContestView,submitContestView,allContestView,contestView
urlpatterns = [
    path('',contestsView),
    path('create/',createContestView),
    path('submit/',submitContestView),
    path('all/',allContestView),
    path('<int:contest_id>/',contestView)
]