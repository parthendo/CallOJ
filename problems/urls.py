from django.urls import path
from .views import correctFormView,dashboardView,problemsView,showProblemView,submitProblemView,createProblemView,aceView

urlpatterns = [ path('',dashboardView,name='dashboard'),
path('thanks/',correctFormView,name='correctForm'),
path('submit/', correctFormView),
path('problems/',problemsView,name='problems'),
path('problems/<int:problem_id>/',showProblemView,name='showProblem'),
path('submission/<int:problem_id>/',submitProblemView,name='submitProblem'),
path('createProblem/',createProblemView,name='createProblem'),
path('ace/',aceView),
]