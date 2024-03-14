from django.db import models
from core import models as core_models
from users import models as user_models
from quesions import models as question_models


# Create your models here.
class CashHistory(core_models.TimeStampModel):
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE, vervose_name="사용자")
    question = models.ForeignKey(question_models.Question, on_delete=models.CASCADE, vervose_name="문제")
    earned = models.IntegerField(vervose_name="획득캐시")
