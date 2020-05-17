from django.db import models
from problems.models import Question
from django.contrib.auth.models import User
# Create your models here.

class Contest(models.Model):
    contestCode = models.CharField(max_length=20)
    contestName = models.CharField(max_length=100)
    startDay = models.IntegerField()
    startMonth = models.IntegerField()
    startYear = models.IntegerField()
    startHours = models.IntegerField()
    startMinutes = models.IntegerField()
    durationHours = models.IntegerField()
    durationMinutes = models.IntegerField()
    rankingStyle = models.IntegerField()
    
    questions = models.ManyToManyField(Question)

class IcpcMarks(models.Model):
    contestId = models.ForeignKey(Contest,default=None,on_delete=models.CASCADE)
    questionId = models.ForeignKey(Question,default=None,on_delete=models.CASCADE)
    userId = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    totalTime = models.IntegerField()
    verdict = models.IntegerField()
