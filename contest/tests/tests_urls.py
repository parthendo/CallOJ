from django.test import SimpleTestCase
from django.urls import reverse, resolve
from contest.views import contestsView,createContestView,submitContestView,allContestView,contestView,showProblemView,submitProblemView,rankListView

class TestUrlsContest(SimpleTestCase):
    def test_initalContestUrl_is_resolved(self):
        url = reverse('initialContestUrl')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,contestsView)

    def test_createContest_url_is_resolved(self):
        url = reverse('createContest')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,createContestView)

    def test_submitContest_url_is_resolved(self):
        url = reverse('submitContest')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,submitContestView)

    def test_allContest_url_is_resolved(self):
        url = reverse('allContest')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,allContestView)

    def test_contest_url_is_resolved(self):
        url = reverse('contest',args=['1'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func,contestView)

    def test_showContestProblem_url_is_resolved(self):
        url = reverse('showContestProblem',args=['1','2'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func,showProblemView)
    
    def test_submitContestProblem_url_is_resolved(self):
        url = reverse('submitContestProblem',args=['1','2'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func,submitProblemView)
    
    def test_ranklist_url_is_resolved(self):
        url = reverse('rankList',args=['1'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func,rankListView)

    
