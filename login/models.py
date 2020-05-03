from django.db import models

# Create your models here.
class User(models.Model):
    userid = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    mail = models.CharField(max_length=50)
    password = models.CharField(max_length=50)