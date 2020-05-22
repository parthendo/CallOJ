from django.test import SimpleTestCase
from django.urls import reverse, resolve
from problems.views import correctFormView,dashboardView,problemsView,showProblemView,submitProblemView,createProblemView,aceView
class TestUrls(SimpleTestCase):
    def test_dashboard_url_is_resolved(self):
        url = reverse('dashboard')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,dashboardView)
    
    def test_correctForm_url_is_resolved(self):
        url = reverse('correctForm')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,correctFormView)

    def test_problems_url_is_resolved(self):
        url = reverse('problems')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,problemsView)

    def test_showProblem_url_is_resolved(self):
        url = reverse('showProblem',args=['1'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func,showProblemView)

    def test_submitProblem_url_is_resolved(self):
        url = reverse('submitProblem',args=['2'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func,submitProblemView)

    def test_createProblem_url_is_resolved(self):
        url = reverse('createProblem')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,createProblemView)

    