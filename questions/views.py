from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny #, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate
from django.conf import settings

from .serializers import QuestionSerializer
from .permissions import IsSelf
from .models import Question


# Create your views here.
class QuestionViewSet(ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):

        admin_permission = ["create", "update", "delete",]
        any_permission = ["retrieve", "list"]

        permission_classes = []
        if self.action in admin_permission:
            permission_classes = [IsAdminUser]
        elif self.action in any_permission:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSelf]

        return [permission() for permission in permission_classes]