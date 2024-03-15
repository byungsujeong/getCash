from import_export.admin import ImportExportMixin

from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Question)
class QuestionAdmin(ImportExportMixin, admin.ModelAdmin):

    """ Question Admin Definition """