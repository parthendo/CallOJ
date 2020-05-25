from django.urls import path
from .views import profileView,updateProfileView,changesToProfileView,showUserProfileView,playlistCategoryProblemsView,addCategoryView,addQuestionToPlaylistView,addCallOjProblemView

urlpatterns = [ path('',profileView,name='initialProfile'),
path('addCategory/',addCategoryView),
path('playlist/<str:playlistCategory>/questions/',playlistCategoryProblemsView,name='categoryQuestions'),
path('<str:playlistCategory>/addQuestion/',addQuestionToPlaylistView),
path('updateProfile/',updateProfileView),
path('changesToProfile/',changesToProfileView),
path('<str:searchedUser>/',showUserProfileView),
path('addCallOjProblem/<int:problemId>/',addCallOjProblemView),
]