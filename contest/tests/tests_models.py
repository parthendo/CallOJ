from django.test import TestCase
from contest.models import Contest,IoiMarks,IcpcMarks
from problems.models import Question
from django.contrib.auth.models import User
class TestModels(TestCase):
    def test_Contest(self):
        problem = Question.objects.create(problemCode="testContestProblem",problemName="testProblem",problemStatement="addAll",timeLimit=2,memoryLimit=65576,marking=1,access=1,creator="Jayant",editorialist="Jayant",totalAttempts=0,successfulAttempts=0)
        contest = Contest.objects.create(contestCode="testContest",contestName="test",startDay=22,startMonth=5,startYear=2020,startHours=21,startMinutes=30,durationHours=5,durationMinutes=10,rankingStyle=1)
        contest.questions.add(problem)
        checkContest = Contest.objects.get(contestCode="testContest")
        self.assertEquals(contest,checkContest)
    
    def test_IoiMarks(self):
        problem = Question.objects.create(problemCode="testProblemIoi",problemName="testProblem",problemStatement="addAll",timeLimit=2,memoryLimit=65576,marking=1,access=1,creator="Jayant",editorialist="Jayant",totalAttempts=0,successfulAttempts=0)
        contest = Contest.objects.create(contestCode="testContestIoi",contestName="test",startDay=22,startMonth=5,startYear=2020,startHours=21,startMinutes=30,durationHours=5,durationMinutes=10,rankingStyle=1)
        user = User.objects.create_user(username="testUserIoi",first_name="ano",last_name="nymous",email="test@gmail.com",password="123")
        ioi = IoiMarks.objects.create(contestId=contest,userId=user,questionId=problem,marksAlloted=100)

    def test_IcpcMarks(self):
        problem = Question.objects.create(problemCode="testProblemIcpc",problemName="testProblem",problemStatement="addAll",timeLimit=2,memoryLimit=65576,marking=1,access=1,creator="Jayant",editorialist="Jayant",totalAttempts=0,successfulAttempts=0)
        contest = Contest.objects.create(contestCode="testContestIcpc",contestName="test",startDay=22,startMonth=5,startYear=2020,startHours=21,startMinutes=30,durationHours=5,durationMinutes=10,rankingStyle=1)
        user = User.objects.create_user(username="testUserIcpc",first_name="ano",last_name="nymous",email="test@gmail.com",password="123")
        icpc = IcpcMarks.objects.create(contestId=contest,userId=user,questionId=problem,totalTime=100,verdict=1)
        testIcpc = IcpcMarks.objects.get(contestId=contest)
        self.assertEquals(icpc,testIcpc)


