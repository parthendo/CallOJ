from django.db import models
from problems.models import Question
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