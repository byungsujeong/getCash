import os
from datetime import timedelta

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.utils import timezone
from django.db.models import Q

from .serializers import QuestionSerializer
from .permissions import IsSelf
from .models import Question
from .pagination import CustomPagination

from cashHistories import models as cashHistory_models


# Create your views here.
class QuestionViewSet(ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class = CustomPagination

    def get_permissions(self):

        admin_permission = ["create", "update", "delete",]
        auth_permission = ["list"]
        any_permission = ["retrieve"]

        permission_classes = []
        if self.action in admin_permission:
            permission_classes = [IsAdminUser]
        elif self.action in any_permission:
            permission_classes = [AllowAny]
        elif self.action in auth_permission:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsSelf]

        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):

        target_date = timezone.now()

        filter_kwargs_qc = {}
        filter_kwargs_qc["user"] = request.user
        filter_kwargs_qc["created__date"] = target_date.date()
        queryset_qc = cashHistory_models.CashHistory.objects.filter(**filter_kwargs_qc)

        quantity_limit = int(os.environ.get('QUANTITY_LIMIT'))

        today_earned = 0
        if queryset_qc:
            for item in queryset_qc:
                today_earned += item.earned
            if today_earned >= quantity_limit:
                return Response({'code': 1, 'message': 'bad request', 'data': None}, status=status.HTTP_400_BAD_REQUEST)

        filter_kwargs_type1 = {'user':request.user}
        filter_kwargs_type2 = {'user':request.user}
        filter_kwargs_type3 = {'user':request.user}

        # filter_kwargs["mid"] = question.mid
        filter_kwargs_type1["created__date"] = target_date.date()

        three_hours_ago = target_date - timedelta(hours=3)
        filter_kwargs_type2["created__gte"] = three_hours_ago

        # tpye1
        cashHistory_type1 = cashHistory_models.CashHistory.objects.filter(**filter_kwargs_type1)
        mid_type1 = set()
        for item in cashHistory_type1:
            mid_type1.add(item.question.mid)
        queryset_type1 = queryset = self.filter_queryset(self.get_queryset()).filter(type='1').exclude(mid__in=mid_type1)

        # type2
        cashHistory_type2 = cashHistory_models.CashHistory.objects.filter(**filter_kwargs_type2)
        mid_type2 = set()
        for item in cashHistory_type2:
            mid_type2.add(item.question.mid)
        queryset_type2 = queryset = self.filter_queryset(self.get_queryset()).filter(type='2').exclude(mid__in=mid_type2)

        # type3
        cashHistory_type3 = cashHistory_models.CashHistory.objects.filter(**filter_kwargs_type3)
        mid_type3 = set()
        for item in cashHistory_type3:
            mid_type3.add(item.question.mid)
        queryset_type3 = queryset = self.filter_queryset(self.get_queryset()).filter(type='3').exclude(mid__in=mid_type3)

        queryset = queryset_type1 | queryset_type2 | queryset_type3
        queryset = queryset.order_by('?')

        page = self.paginate_queryset(queryset[:3])
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)