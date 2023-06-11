from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


# Create your models here.

class TeamsModel(models.Model):
    team_name = models.CharField(max_length=80, unique=True)
    logo = models.URLField()
    team_mood_rate = models.DecimalField(max_digits=6, decimal_places=3, null=True)


class UserModel(AbstractUser):
    first_name = models.CharField(max_length=80, unique=True)
    last_name = models.CharField(max_length=80)
    team = models.ForeignKey(TeamsModel, on_delete=models.CASCADE, null=True)
    avarage_mood_mark = models.IntegerField(null=True)
    username = models.CharField(unique=True, max_length=20)
    token_id = models.OneToOneField(Token, on_delete=models.CASCADE, null=True)


# class UserAdminModel(AbstractUser):
#     username=models.CharField(unique=True, max_length=20)


class HappyModel(models.Model):
    mood_mark = models.IntegerField(null=False)
    day = models.DateField(default=datetime.utcnow, null=False)
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=False)
