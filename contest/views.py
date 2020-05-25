from django.shortcuts import render
from problems.models import Question
from .models import Contest, IcpcMarks, IoiMarks
from problems.models import Question
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta
from problems.judge import Judge
from problems.utils import Utils
from django.contrib.auth.models import User
from .utils import ContestUtilities
from problems.utils import Utils
import os, zipfile
import shutil
import time
from OJ.loggingUtils import get_client_ip
from OJ.loggingUtils import registerLog
# Create your views here.
def contestsView(request):
    return render(request,'thanks.html')

def createContestView(request):
    questions = Question.objects.all()
    all_questions = []
    for question in questions:
        if question.access == 1 or question.creator == request.user.username:
            print("Hello")
            all_questions.append(question)
    registerLog('INFO','GET',request.user.username,'createContest','creatingContest',get_client_ip(request))
    return render(request,'createContest.html',{'all_problems':all_questions})

def submitContestView(request):
    contestCode = request.POST['contestCode']
    contestName = request.POST['contestName']
    startDay = request.POST['day']
    startMonth = request.POST['month']
    startYear = request.POST['year']
    startHours = request.POST['start_hours']
    startMinutes = request.POST['start_minutes']
    durationHours = request.POST['hours']
    durationMinutes = request.POST['minutes']
    marking = request.POST['marking']
    if marking == "IOI":
        rankingStyle = 1
    if marking == "ICPC":
        rankingStyle = 2

    all_contests = Contest.objects.all()
    contest_exists = 0
    for contest in all_contests:
        if contest.contestCode == contestCode:
            contest_exists = 1
            break

    if contest_exists == 1:
        return HttpResponseRedirect('/contest/create/')
    contest = Contest(contestCode=contestCode,contestName=contestName,startDay=startDay,startMonth=startMonth,startYear=startYear,startHours=startHours,startMinutes=startMinutes,durationHours=durationHours,durationMinutes=durationMinutes,rankingStyle=rankingStyle)
    contest.save()
    checked_questions = request.POST.getlist('checks[]')
    print(request.POST)

    #all_problems = Quesion.objects.all()
    for question in checked_questions:
        problem = Question.objects.get(problemCode=str(question))
        registerLog('INFO','POST',request.user.username,'Contest','AddedQuestion_'+str(problem.problemCode),get_client_ip(request))
        contest.questions.add(problem)

    print(contest.questions.all())
    all_questions = contest.questions.all()
    for question in all_questions:
        print(question.problemCode)
    # question_instance = Contest.objects.filter(questions__problemCode="ADDALL")
    # print(question_instance.problemCode)
    registerLog('INFO','POST',request.user.username,'Contest','ContestMarkingStyle_'+str(marking),get_client_ip(request))
    registerLog('INFO','POST',request.user.username,'Contest','successfullyCreatedContest',get_client_ip(request))
    return HttpResponseRedirect('/contest/all/')

def allContestView(request):
    util = ContestUtilities()
    present_contests,future_contests = util.getContests()
    return render(request,'allContests.html',{'present':present_contests,'future':future_contests})

def contestView(request,contest_id):
    util = ContestUtilities()
    contestStatus = util.contestFinished(contest_id)
    current_contest = Contest.objects.get(id=contest_id)
    all_questions = current_contest.questions.all()
    return render(request,'contestQuestions.html',{'all_problems':all_questions,'contestId':contest_id,'status':contestStatus})

def showProblemView(request,contest_id,problem_id):
    registerLog('INFO','POST',request.user.username,'Contest'+str((Contest.objects.get(id=contest_id)).contestCode),'atLeastCameToContest',get_client_ip(request))
    util = ContestUtilities()
    languages = Utils.fetchAvailableLanguages(None)
    contestStatus = util.contestFinished(contest_id)
    problem_to_show = Question.objects.get(id=problem_id)
    if contestStatus == "contestEnded":
        return render(request,'problem.html',{'problem':problem_to_show})
    else:
        return render(request,'problem.html',{'problem':problem_to_show,'contestId':contest_id,'languages':languages})

def submitProblemView(request,contest_id,problem_id):
    registerLog('INFO','POST',request.user.username,'Contest'+str((Contest.objects.get(id=contest_id)).contestCode),'AtLeastSubmittedOneProblem',get_client_ip(request))
    registerLog('INFO','POST',request.user.username,'Contest'+str((Contest.objects.get(id=contest_id)).contestCode),'AttemptedProblem'+str((Question.objects.get(id=problem_id)).problemCode),get_client_ip(request))
    usercode = request.POST['code']
    print(usercode)
    language = request.POST['language']
    problem = Question.objects.get(id=problem_id)
    utils = Utils()
    contestUtil = ContestUtilities()
    x = utils.submitProblem(request.user, usercode, language, problem)
    print(x)
    print('Hello',len(x))
    print(x[0][0])
    contestUtil.submitProblem(x,contest_id,problem_id,request)
    if x[len(x)-1][0]=="AC":
        registerLog('INFO','POST',request.user.username,'Contest'+str((Contest.objects.get(id=contest_id)).contestCode),'CorrectAnswerFor_'+str(problem.problemCode),get_client_ip(request))
    elif x[0]=='CE':
        registerLog('INFO','POST',request.user.username,'Contest'+str((Contest.objects.get(id=contest_id)).contestCode),'CompilationErrorFor_'+str(problem.problemCode),get_client_ip(request))
    else:
        registerLog('INFO','POST',request.user.username,'Contest'+str((Contest.objects.get(id=contest_id)).contestCode),'WrongAnswerFor_'+str(problem.problemCode),get_client_ip(request))
    if(x[0]=='CE'):
            temp = []
            errorMessage = " "
            temp.append("Compilation Error")
            for messageString in x[4]:
                errorMessage = errorMessage + messageString + "    "
            temp.append(errorMessage)
            x=[]
            x.append(temp)
    languages = Utils.fetchAvailableLanguages(None)
    return render(request,'problem.html',{'problem':problem,'languages': languages,'results':x,'usercode':usercode,'languageUsed':language,'resultLength':len(x)})

def rankListView(request,contest_id):
    currentContest = Contest.objects.get(id=contest_id)
    util = ContestUtilities()
    registerLog('INFO','POST',request.user.username,'Contest'+str(currentContest.contestCode),'PartOfRanklist',get_client_ip(request))
    if currentContest.rankingStyle == 1:
        final_list = util.ioiRanklist(contest_id)
        contest_type = 1
        return render(request,"ranklist.html",{'rankings':final_list,'ioi':contest_type,'currentContest':currentContest})
    else:
        print('Rajjo')
        final_list = util.icpcRanklist(contest_id)
        contest_type = 2 
        return render(request,"ranklist.html",{'rankings':final_list,'currentContest':currentContest})




