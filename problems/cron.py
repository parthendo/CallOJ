from contest.models import Contest
from .models import Question
import time
from contest.utils import ContestUtilities

def makePublic():
	allContests = Contest.objects.all()
	contestUtilities = ContestUtilities()
	for contests in allContests:
		if(contestUtilities.contestFinished(contests.ID) == 0):
			contestQuestions = contests.questions.all()
			for question in contestQuestions:
				question.access = 1
				question.save()

