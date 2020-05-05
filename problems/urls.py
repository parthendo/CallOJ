from django.urls import path
from .views import correct_form,dashboard,problems,showProblemView,submitProblemView,createProblemView

urlpatterns = [ path('',dashboard),
path('thanks/',correct_form),
path('submit/', correct_form),
path('problems/',problems),
path('problems/<int:problem_id>/',showProblemView),
path('submission/<int:problem_id>/',submitProblemView),
path('createProblem/',createProblemView),]