from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.CashHistory)
class CashHistoryAdmin(admin.ModelAdmin):

    """ CashHistory Admin Definition """