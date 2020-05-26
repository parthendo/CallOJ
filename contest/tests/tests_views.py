from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from contest.models import Contest,IoiMarks,IcpcMarks
import json

class TestViews(TestCase):
    def test_contests(self):
        client = Client()
        response = client.get(reverse('initialContestUrl'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'thanks.html')
    
    def test_createContest(self):
        client = Client()
        response = client.get(reverse('createContest'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'createContest.html')

    def test_allContest(self):
        client = Client()
        response = client.get(reverse('allContest'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'allContests.html')

    def test_submitContest(self):
        client = Client()
        response = self.client.post(reverse('submitContest'),data={'contestCode':'anonymous','contestName':'123','day':'22','month':'5','year':'2020','start_hours':'21','start_minutes':'30','hours':'1','minutes':'30','marking':'IOI'})
        self.assertEquals(response.status_code,302)

    # def test_contest(self):
    #     client = Client()
    #     Contest.objects.create(contestCode="test",contestName="test",startDay=22,startMonth=5,startYear=2020,startHours=21,startMinutes=30,durationHours=5,durationMinutes=10,rankingStyle=1)
    #     response = client.get(reverse('contest',args=['1']))
    #     self.assertEquals(response.status_code,200)
    #     self.assertTemplateUsed(response,'contestQuestions.html')
    
    # def test_contestShowProblem(self):
    #     client = Client()
    #     response = client.get(reverse('showContestProblem',args=['1','2']))
    #     self.assertEquals(response.status_code,200)
    #     self.assertTemplateUsed(response,'problem.html')



