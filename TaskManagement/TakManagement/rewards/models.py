from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Reward(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    coins = models.PositiveIntegerField(default=0)
    reason = models.CharField(max_length=255)
    date_awarded = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task_title = models.CharField(max_length=255)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comments = models.TextField(blank=True)
    date_submitted = models.DateTimeField(auto_now_add=True)

        

    

