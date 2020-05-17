from django.shortcuts import render
from problems.models import Question
from .models import Contest, IcpcMarks, IoiMarks
from problems.models import Question
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta
from problems.judge import Judge
from django.contrib.auth.models import User
from .utils import ContestUtilities
import os, zipfile
import shutil
import time
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
        contest.questions.add(problem)

    print(contest.questions.all())
    all_questions = contest.questions.all()
    for question in all_questions:
        print(question.problemCode)
    # question_instance = Contest.objects.filter(questions__problemCode="ADDALL")
    # print(question_instance.problemCode)
    return render(request,'thanks.html')

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
    util = ContestUtilities()
    contestStatus = util.contestFinished(contest_id)
    problem_to_show = Question.objects.get(id=problem_id)
    if contestStatus == "contestEnded":
        return render(request,'problem.html',{'problem':problem_to_show})
    else:
        return render(request,'problem.html',{'problem':problem_to_show,'contestId':contest_id})

def submitProblemView(request,contest_id,problem_id):
    usercode = request.POST['code']
    language = request.POST['language']
    problem = Question.objects.get(id=problem_id)
    if language == "Java":
        with open(("media/submittedFiles/"+request.user.username+"/"+problem.problemCode+".txt"), "w") as file:
            file.write(usercode)
        my_file = "media/submittedFiles/"+request.user.username+"/"+problem.problemCode+".txt"
        base = os.path.splitext(my_file)[0]
        os.rename(my_file, base + '.java')
    if language == "C++":
        with open(("media/submittedFiles/"+request.user.username+"/"+problem.problemCode+".txt"), "w") as file:
            file.write(usercode)
        my_file = "media/submittedFiles/"+request.user.username+"/"+problem.problemCode+".txt"
        base = os.path.splitext(my_file)[0]
        os.rename(my_file, base + '.cpp')
    if language == "python":
        with open(("media/submittedFiles/"+request.user.username+"/"+problem.problemCode+".txt"), "w") as file:
            file.write(usercode)
        my_file = "media/submittedFiles/"+request.user.username+"/"+problem.problemCode+".txt"
        base = os.path.splitext(my_file)[0]
        os.rename(my_file, base + '.py')
    if language == "C":
        with open(("media/submittedFiles/"+request.user.username+"/"+problem.problemCode+".txt"), "w") as file:
            file.write(usercode)
        my_file = "media/submittedFiles/"+request.user.username+"/"+problem.problemCode+".txt"
        base = os.path.splitext(my_file)[0]
        os.rename(my_file, base + '.c')

    judge = Judge()
    judge.judgeConfigFile =  b"/home/jayant/CallOJ/media/judgeConfiguration/config.yml"
    if language == "Java":
        judge.solutionCode = request.user.username + "/" + problem.problemCode + ".java"
    if language == "C++":
        judge.solutionCode = request.user.username + "/" + problem.problemCode + ".cpp"
    if language == "C":
        judge.solutionCode = request.user.username + "/" + problem.problemCode + ".c"
    if language == "python":
        judge.solutionCode = request.user.username + "/" + problem.problemCode + ".py"

    judge.problemCode = str(problem.problemCode)
    # judge.problemCode = "XYZ"
    if language == "Java":
        judge.languageCode = "JAVA8"

    judge.timeLimit = str(problem.timeLimit)
    judge.memoryLimit = str(problem.memoryLimit)
    judge.problemType = problem.marking #ICPC type
    x = judge.executeJudge()
    print(x)
    print('Hello',len(x))
    final_verdict = x[len(x)-1][0]
    marks_obtained = x[len(x)-1][1]
    #Add Code to check whether contest finished or not , if not finished then only update in Icpc_Marks

    contest = Contest.objects.get(id=contest_id)
    print('Ho',contest_id)
    startYear = contest.startYear
    startMonth = contest.startMonth
    startDay = contest.startDay
    startHours = contest.startHours
    startMinutes = contest.startMinutes
    entries = IcpcMarks.objects.all()
    entries_ioi = IoiMarks.objects.all()
    print(entries)
    entry = ()
    entry_ioi = ()
    for item in entries:
        if item.userId_id == request.user.id and item.contestId_id == contest_id and item.questionId_id==problem_id:
            entry = item
            break
    for item in entries_ioi:
        if item.userId_id == request.user.id and item.contestId_id == contest_id and item.questionId_id==problem_id:
            entry_ioi = item
            break
    #1 is for Icpc
    if contest.rankingStyle == 2:
        # entry = IcpcMarks.objects.get(userId_id=request.user.id,contestId_id=contest_id,questionId_id=problem_id)
        if entry:
            if final_verdict == "AC":
                entry.verdict = 1
                datetimeFormat = '%Y-%m-%d %H:%M:%S'
                now = datetime.now()
                current = str(now)
                current = current[0:19]
                # server_year = current[:4]
                # server_month = current[5:7]
                # server_day = current[8:10]
                # server_hours = current[11:13]
                # server_minutes = current[14:16]
                # server_seconds = current[17:19]
                contestStart = str(startYear)+ "-" + str(startMonth)+ "-" + str(startDay)+" "+str(startHours)+ ":"+str(startMinutes)+":"+ "00"
                timeToSolve = datetime.strptime(current, datetimeFormat)-datetime.strptime(contestStart, datetimeFormat)
                print("contestStart:",contestStart)
                entry.totalTime = entry.totalTime + timeToSolve.seconds
                entry.save()
            else:
                entry.totalTime = entry.totalTime + 1200
                entry.save()
        else:
            if final_verdict == "AC":
                verdict = 1
                datetimeFormat = '%Y-%m-%d %H:%M:%S'
                now = datetime.now()
                current = str(now)
                current = current[0:19]
                contestStart = str(startYear) + "-" + str(startMonth) + "-" + str(startDay) + " " + str(startHours) + ":" + str(startMinutes) + ":" + "00"
                print('HelloJayant')
                print(contestStart)
                timeToSolve = datetime.strptime(current, datetimeFormat)-datetime.strptime(contestStart, datetimeFormat)
                # contest_object = Contest.objects.get(id=contest_id)
                # problem_object = Question.objects.get(id=problem_id)
                # user_object = User.objects.get(id=request.user.id)
                newItem = IcpcMarks(userId_id=request.user.id,contestId_id=contest_id,questionId_id=problem_id,totalTime=timeToSolve.seconds,verdict=verdict)
                newItem.save()
            else:
                verdict = 0
                contest_object = Contest.objects.get(id=contest_id)
                problem_object = Question.objects.get(id=problem_id)
                user_object = User.objects.get(id=request.user.id)
                newItem = IcpcMarks(userId_id=request.user.id,contestId_id=contest_id,questionId_id=problem_id,totalTime=1200,verdict=verdict)
                newItem.save()
    else:
        if entry_ioi:
            entry_ioi.marksAlloted = max(entry_ioi.marksAlloted,marks_obtained)
            entry_ioi.save()
        else:
            newItem = IoiMarks(userId_id=request.user.id,contestId_id=contest_id,questionId_id=problem_id,marksAlloted=marks_obtained)
            newItem.save()



    print(x[0][0])
    return render(request,'results.html',{'results':x})

def rankListView(request,contest_id):
    currentContest = Contest.objects.get(id=contest_id)
    util = ContestUtilities()
    if currentContest.rankingStyle == 1:
        final_list = util.ioiRanklist(contest_id)
        contest_type = 1
        return render(request,"ranklist.html",{'rankings':final_list,'ioi':contest_type})
    else:
        print('Rajjo')
        final_list = util.icpcRanklist(contest_id)
        contest_type = 2 
        return render(request,"ranklist.html",{'rankings':final_list})

    





