from django.test import TestCase
from problems.models import Question
class TestModels(TestCase):
    def test_Question(self):
        question = Question.objects.create(problemCode="test",problemName="testProblem",problemStatement="addAll",timeLimit=2,memoryLimit=65576,marking=1,access=1,creator="Jayant",editorialist="Jayant",totalAttempts=0,successfulAttempts=0)
        question2 = Question.objects.create(problemCode="tost",problemName="testProblem",problemStatement="addAll",timeLimit=2,memoryLimit=65576,marking=1,access=1,creator="Jayant",editorialist="Jayant",totalAttempts=0,successfulAttempts=0)
        createdQuestion = Question.objects.get(problemCode="test")
        self.assertEquals(question,createdQuestion)