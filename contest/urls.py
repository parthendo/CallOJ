from django.urls import path, include
from .views import contestsView,createContestView,submitContestView,allContestView,contestView,showProblemView,submitProblemView,rankListView
urlpatterns = [
    path('',contestsView),
    path('create/',createContestView),
    path('submit/',submitContestView),
    path('all/',allContestView),
    path('<int:contest_id>/',contestView),
    path('<int:contest_id>/<int:problem_id>/',showProblemView),
    path('<int:contest_id>/<int:problem_id>/submit/',submitProblemView),
    path('<int:contest_id>/ranklist/',rankListView),
]