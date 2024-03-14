from django.db import models
from core import models as core_models


# Create your models here.
class Question(core_models.TimeStampModel):

    """ Question Model Definition """

    TYPE1 = 1
    TYPE2 = 2
    TYPE3 = 3

    TYPE_CHOICES = [
        (TYPE1, '타입1'),
        (TYPE2, '타입2'),
        (TYPE3, '타입3'),
    ]
    
    title = models.CharField(max_length=255, verbose_name="제목")
    answer = models.CharField(max_length=255, verbose_name="정답")
    mid = models.CharField(max_length=255, verbose_name="범주")
    quantity = models.IntegerField(verbose_name="수량")
    type = models.IntegerChoices(choices=TYPE_CHOICES, verbose_name="타입")

