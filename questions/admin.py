from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):

    """ Question Admin Definition """