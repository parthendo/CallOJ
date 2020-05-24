from django.db import models
from django.contrib.auth.models import User
from problems.models import PlaylistProblems
# Create your models here.
class UserPlaylist(models.Model):
    userId = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    playlistCategory = models.CharField(max_length=200)
    problems = models.ManyToManyField(PlaylistProblems)
    problemCount = models.IntegerField()