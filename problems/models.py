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