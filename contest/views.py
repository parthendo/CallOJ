from django.shortcuts import render
from problems.models import Question
from .models import Contest
from django.http import HttpResponseRedirect
from datetime import datetime
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
    all_contests = Contest.objects.all()
    present_contests = []
    future_contests = []
    past_contests = []
    now = datetime.now()
    current = str(now)
    server_year = current[:4]
    server_month = current[5:7]
    server_day = current[8:10]
    server_hours = current[11:13]
    server_minutes = current[14:16]
    print('Hi',server_year,server_month,server_day,server_hours,server_minutes)
    print('Holla',int(server_year),int(server_month),int(server_day),int(server_hours),int(server_minutes))
    for contest in all_contests:
        if contest.startYear>int(server_year):
            future_contests.append(contest)
            continue
        if contest.startMonth>int(server_month):
            future_contests.append(contest)
            continue
        if contest.startDay>int(server_day):
            future_contests.append(contest)
            continue
        if contest.startHours>int(server_hours):
            future_contests.append(contest)
            continue
        if contest.startMinutes>int(server_minutes):
            future_contests.append(contest)
            continue
        present_contests.append(contest)
    
    return render(request,'allContests.html',{'present':present_contests,'future':future_contests})

def contestView(request,contest_id):
    current_contest = Contest.objects.get(id=contest_id)
    all_questions = current_contest.questions.all()
    return render(request,'contestQuestions.html',{'all_problems':all_questions})




