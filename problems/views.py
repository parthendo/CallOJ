from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import AllProblems,Question
from .judge import Judge
import os, zipfile
import shutil
import time
from .utils import Utils
from userprofile.models import UserPlaylist

from django.core.files.storage import FileSystemStorage
from OJ.loggingUtils import registerLog
from OJ.loggingUtils import get_client_ip

@login_required
def correctFormView(request):
    return render(request,'thanks.html')

@login_required
def dashboardView(request):
    return render(request,'dashboard.html')

@login_required
def problemsView(request):
    questions = Question.objects.all()
    allEntriesInUserPlaylist = UserPlaylist.objects.all()
    categories = []
    for entry in allEntriesInUserPlaylist:
        if entry.userId_id == request.user.id:
            categories.append(entry.playlistCategory)
    all_questions = []
    registerLog('INFO','GET',request.user.username,'Problem','ViewProblemList',get_client_ip(request))
    for ques in questions:
        if ques.access == 1 or ques.creator == request.user.username:
            all_questions.append(ques)
    return render(request,'problems.html',{'all_problems':all_questions,'categories':categories})

@login_required
def showProblemView(request,problem_id):
    problem_to_show = Question.objects.get(id=problem_id)
    languages = Utils.fetchAvailableLanguages(None)
    registerLog('INFO','GET',request.user.username,'Problem','AccessProblemWithID_'+str(problem_id),get_client_ip(request))
    return render(request,'problem.html',{'problem':problem_to_show, 'languages': languages})

@login_required
def submitProblemView(request,problem_id):
    if request.method == 'POST':
        usercode = request.POST['code']
        print(usercode)
        language = request.POST['language']
        registerLog('INFO','POST',request.user.username,'Problem','SubmittedProblemWithID_'+str(problem_id),get_client_ip(request))
        registerLog('INFO','POST',request.user.username,'Problem',language,get_client_ip(request))
        registerLog('INFO','POST',request.user.username,'Problem','Problem'+str(problem_id)+'_Language'+language,get_client_ip(request))
        problem = Question.objects.get(id=problem_id)
        utils = Utils()
        x = utils.submitProblem(request.user, usercode, language, problem)
        registerLog('INFO','POST',request.user.username,'Problem','JudgeExecutedForProblemWithID_'+str(problem_id),get_client_ip(request))
        problem.totalAttempts = problem.totalAttempts + 1
        if x[len(x)-1][0] == "AC":
            problem.successfulAttempts = problem.successfulAttempts + 1
            registerLog('INFO','POST',request.user.username,'Problem','ForProblemWithID_'+str(problem_id)+'verdict_AC',get_client_ip(request))
        problem.save()
        print(x)
        if(x[0]=='CE'):
            temp = []
            errorMessage = " "
            temp.append("Compilation Error")
            registerLog('INFO','POST',request.user.username,'Problem','ForProblemWithID_'+str(problem_id)+'verdict_CE',get_client_ip(request))
            for messageString in x[4]:
                errorMessage = errorMessage + messageString + "    "
            temp.append(errorMessage)
            x=[]
            x.append(temp)
        languages = Utils.fetchAvailableLanguages(None)
        return render(request,'problem.html',{'problem':problem,'languages': languages,'results':x,'usercode':usercode,'languageUsed':language,'resultLength':len(x)})

@login_required
def createProblemView(request):
    if request.method == 'POST':
        exists = 0
        fileValidity = True
        yml_file = request.FILES['uploadFiles']
        for f in request.FILES.getlist('uploadFiles'):
            filename = f.name
            reqname = "init.yml"
            if filename == reqname:
                print()
            else:
                registerLog('ERROR','POST',request.user.username,'Problem','CreateProblem_Invalid_initYAML',get_client_ip(request))
                print("not yml")

        for f in request.FILES.getlist('uploadedFiles'):
            filename = f.name
            length = len(filename)
            if filename[length-1]!='t' or filename[length-2]!='x' or filename[length-3]!='t' or filename[length-4]!='.':
                fileValidity = False
                registerLog('ERROR','POST',request.user.username,'Problem','CreateProblem_Invalid_testCase',get_client_ip(request))
                break
        if fileValidity == True:
            problem_code = request.POST['problemCode']
            problem_name = request.POST['problemName']
            problem_statement = request.POST['problemStatement']
            time_limit = request.POST['timeLimit']
            memory_limit = request.POST['memoryLimit']
            problemType = request.POST['problemType']
            print(int(problemType))
            if int(problemType) == 1:
                marking = 1
            else:
                marking = 2
            visibility = request.POST['visibility']
            print(int(visibility))
            if int(visibility) == 1:
                access = 1
            else:
                access = 2
            creator = request.user.username
            all_questions = Question.objects.all()
            for ques in all_questions:
                if ques.problemCode == problem_code:
                    exists = 1
                    break
            if exists == 1:
                return render(request,'createproblem.html')

            all_files = request.FILES.getlist('uploadedFiles')
            utils = Utils()
            utils.saveProblem(yml_file, problem_code, all_files)
            registerLog('INFO','POST',request.user.username,'Problem','CreateProblemSuccessful',get_client_ip(request))
            registerLog('INFO','POST',request.user.username,'Problem','CreateProblem_'+problem_code,get_client_ip(request))
            newProblem = Question(problemCode=problem_code,problemName=problem_name,problemStatement=problem_statement,timeLimit=time_limit,memoryLimit=memory_limit,marking=marking,access=access,creator=creator,editorialist=creator,totalAttempts=0,successfulAttempts=0)
            newProblem.save()
            return HttpResponseRedirect('/dashboard/problems/')
        else:
            print("Not valid input cases")

    return render(request,'createproblem.html')

def aceView(request):
    return render(request,'demoAce.html')

