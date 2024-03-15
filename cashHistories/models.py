from django.db import models
from core import models as core_models
from users import models as user_models
from questions import models as question_models


# Create your models here.
class CashHistory(core_models.TimeStampModel):

    CORRECT = 1
    INCORRECT = 0

    STATUS_CHOICES = [
        (CORRECT, '정답'),
        (INCORRECT, '오답'),
    ]

    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE, verbose_name="사용자")
    question = models.ForeignKey(question_models.Question, on_delete=models.CASCADE, verbose_name="문제")
    submittedAnswer = models.CharField(max_length=255, null=True, verbose_name="제출정답")
    status = models.IntegerField(choices=STATUS_CHOICES, default=INCORRECT, verbose_name="상태")
    earned = models.IntegerField(verbose_name="획득캐시")
