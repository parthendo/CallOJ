from django.urls import path, include
from .views import contestsView,createContestView,submitContestView,allContestView,contestView,showProblemView,submitProblemView,rankListView

urlpatterns = [
    path('',contestsView,name='initialContestUrl'),
    path('create/',createContestView,name='createContest'),
    path('submit/',submitContestView,name='submitContest'),
    path('all/',allContestView,name='allContest'),
    path('<int:contest_id>/',contestView,name='contest'),
    path('<int:contest_id>/<int:problem_id>/',showProblemView,name='showContestProblem'),
    path('<int:contest_id>/<int:problem_id>/submit/',submitProblemView,name='submitContestProblem'),
    path('<int:contest_id>/ranklist/',rankListView,name='rankList'),
]