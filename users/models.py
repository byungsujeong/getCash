from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):

    """ Custom User Model """

    username = models.EmailField(max_length=254, unique=True, verbose_name="이메일")
    cash = models.IntegerField(default=0, verbose_name="캐시")
    # questionList = models.ManyToManyField()