import os
from datetime import timedelta

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from django.utils import timezone

from users import models as user_models

from .serializers import CashHistorySerializer, ReadOnlyCashHistorySerializer
from .models import CashHistory
from .pagination import CustomPagination

from questions import models as question_models


# Create your views here.
class CashHistoryViewSet(ModelViewSet):

    queryset = CashHistory.objects.all()
    serializer_class = CashHistorySerializer
    pagination_class = CustomPagination

    def get_permissions(self):

        auth_permission = ["create", "list", "correct"]

        permission_classes = []
        if self.action in auth_permission:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):

        question_id = request.data.get("question_id")

        try:
            question = question_models.Question.objects.get(id=question_id)
        except question_models.Question.DoesNotExist:
            return Response({'code': 1, 'message': 'not found', 'data': None}, status=status.HTTP_404_NOT_FOUND)
        
        target_date = timezone.now()

        # quantity check
        filter_kwargs_qc = {}
        filter_kwargs_qc["user"] = request.user
        filter_kwargs_qc["created__date"] = target_date.date()
        queryset_qc = self.filter_queryset(self.get_queryset()).filter(**filter_kwargs_qc)

        quantity_limit = int(os.environ.get('QUANTITY_LIMIT'))

        today_earned = 0
        if queryset_qc:
            for item in queryset_qc:
                today_earned += item.earned
            if today_earned >= quantity_limit:
                return Response({'code': 1, 'message': 'bad request', 'data': None}, status=status.HTTP_400_BAD_REQUEST)

        filter_kwargs = {}
        filter_kwargs["user"] = request.user
        filter_kwargs["question__mid"] = question.mid

        submittedAnswer = request.data.get('submittedAnswer')
        new_data = request.data
        new_data['status'] = 0
        new_data['earned'] = 0
        new_data['user'] = request.user.id
        new_data['question'] = question_id

        if question.type == '1':
            filter_kwargs["created__date"] = target_date.date()
            if question.answer == submittedAnswer:
                new_data['status'] = 1
                new_data['earned'] = question.quantity
        elif question.type == '2':
            three_hours_ago = target_date - timedelta(hours=3)
            filter_kwargs["created__gte"] = three_hours_ago
            if question.answer == submittedAnswer:
                new_data['status'] = 1
                new_data['earned'] = question.quantity
        elif question.type == '3':
            if f'{question.title}a' == submittedAnswer:
                new_data['status'] = 1
                new_data['earned'] = question.quantity
        else:
            if f'{question.title}new' == submittedAnswer:
                new_data['status'] = 1
                new_data['earned'] = question.quantity
          
        queryset = self.filter_queryset(self.get_queryset()).filter(**filter_kwargs)
        if queryset:
            return Response({'code': 1, 'message': 'bad request', 'data': None}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if serializer.data['status'] == 1:
            user_instance = user_models.User.objects.get(pk=request.user.pk)
            user_instance.cash = user_instance.cash + question.quantity
            user_instance.save()
        return Response({'code': 0, 'message': None, 'data': serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(user=request.user)[:3]
        if queryset:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = ReadOnlyCashHistorySerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = ReadOnlyCashHistorySerializer(queryset, many=True)
            return Response({'code': 0, 'message': None, 'data': serializer.data})
        
        return Response({'code': 1, 'message': 'not found', 'data': None}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=["get"])
    def correct(self, request):
        filter_kwargs = {}
        filter_kwargs["user"] = request.user
        filter_kwargs['status'] = 1
        queryset = self.filter_queryset(self.get_queryset()).filter(**filter_kwargs)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ReadOnlyCashHistorySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ReadOnlyCashHistorySerializer(queryset, many=True)
        return Response({'code': 0, 'message': None, 'data': serializer.data})
    