import json

from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from .models import CashHistory

from users import models as user_models
from questions import models as question_models


# Create your tests here.
class CashHistoryViewSetTestCase(TestCase):
    def setUp(self):
        self.user = user_models.User.objects.create_user(username='test@test.com', password='test1234')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_cash_history(self):
        question = question_models.Question.objects.create(title="newTitle4", answer="newAnswer4", mid="newMid4", quantity=40, type="4")
        data = {
            "question_id": question.id,
            "submittedAnswer": "newTitle4new"
        }
        response = self.client.post('/api/v1/cashHistories/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 생성된 CashHistory 확인
        cash_history = CashHistory.objects.last()
        self.assertEqual(cash_history.user, self.user)
        self.assertEqual(cash_history.question, question)
        self.assertEqual(cash_history.status, 1)
        self.assertEqual(cash_history.earned, 40)

    def test_create_cash_history_with_invalid_question(self):
        data = {
            "question_id": 999,
            "submittedAnswer": "newTitle4new"
        }
        response = self.client.post('/api/v1/cashHistories/', data=json.dumps(data), content_type='application/json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_cash_history_exceed_limit(self):
        question = question_models.Question.objects.create(title="newTitle5", answer="newAnswer", mid="newMid5", quantity=110, type="5")
        
        for _ in range(5):
            CashHistory.objects.create(user=self.user, question=question, status=1, earned=20)

        data = {
            "question_id": question.id,
            "submittedAnswer": "newTitle5new"
        }
        response = self.client.post('/api/v1/cashHistories/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
