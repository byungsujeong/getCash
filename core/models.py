from django.db import models


# Create your models here.
class TimeStampModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")
    updated = models.DateTimeField(auto_now=True, verbose_name="수정일시")

    class Meta:
        abstract = True