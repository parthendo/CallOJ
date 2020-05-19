from django.urls import path
from .views import correctFormView,dashboardView,problemsView,showProblemView,submitProblemView,createProblemView,aceView

urlpatterns = [ path('',dashboardView),
path('thanks/',correctFormView),
path('submit/', correctFormView),
path('problems/',problemsView),
path('problems/<int:problem_id>/',showProblemView),
path('submission/<int:problem_id>/',submitProblemView),
path('createProblem/',createProblemView),
path('ace/',aceView),
]