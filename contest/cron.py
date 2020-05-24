from .emailAlert import alertEmail
from django.contrib.auth.models import User
from contest.models import Contest
from contest.utils import ContestUtilities

def contestAlert():

	contestUtilities = ContestUtilities()
	upcomingContest = False
	contests = Contest.objects.all()
	for contest in contests:
		if(contestUtilities.contestState(contest.id) == 1):
			upcomingContest = True
	print(upcomingContest)
	if(upcomingContest == True):
		emailList = []
		allUser = User.objects.all()
		for user in allUser:
			emailList.append(user.email)
		mail = alertEmail()
		mail.alertMassUsers(emailList,'Contest Update','Hi fellow IIITBian,\n\nThis is just to tell you that a contest awaits for you in the future. Hope you check it out CallOJ\'s upcoming contests and mark your calendar accordingly.\nSee you on the ranklist!\n\nGod Speed\nCallOJ')