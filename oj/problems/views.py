from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from .models import AllProblems
# Create your views here.
def correct_form(request):
    return render(request,'thanks.html')

def dashboard(request):
    return render(request,'dashboard.html')

def problems(request):
    all_questions = AllProblems.objects.all()
    return render(request,'problems.html',{'all_problems':all_questions})

def showProblemView(request,problem_id):
    problem_to_show = AllProblems.objects.get(id=problem_id)
    return render(request,'problem.html',{'problem':problem_to_show})

def submitProblemView(request,problem_id):
    usercode = request.POST['code']
    language = request.POST['language']
    print(usercode,language)
    return render(request,'thanks.html')
