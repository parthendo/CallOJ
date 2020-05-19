from django.db import models

# Create your models here.
class AllProblems(models.Model):
    problemCode = models.CharField(max_length=50)
    problemName = models.CharField(max_length=100)
    problemStatement = models.TextField()
    timeLimit = models.FloatField()
    memoryLimit = models.IntegerField()
    creator = models.CharField(max_length=20)
    editorialist = models.CharField(max_length=20)

class Question(models.Model):
    problemCode = models.CharField(max_length=50)
    problemName = models.CharField(max_length=100)
    problemStatement = models.TextField()
    timeLimit = models.FloatField()
    memoryLimit = models.IntegerField()
    marking = models.IntegerField()
    access = models.IntegerField()
    creator = models.CharField(max_length=20)
    editorialist = models.CharField(max_length=20)
    totalAttempts = models.IntegerField()
    successfulAttempts = models.IntegerField()



