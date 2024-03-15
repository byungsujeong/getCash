import jwt

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny #, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate
from django.conf import settings

from .serializers import UserSerializer
from .permissions import IsSelf
from .models import User


# Create your views here.
class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):

        admin_permission = ["list",]
        any_permission = ["create", "retrieve", "login",]

        permission_classes = []
        if self.action in admin_permission:
            permission_classes = [IsAdminUser]
        elif self.action in any_permission:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSelf]

        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            encode_jwt = jwt.encode({"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256")
            return Response(data={'token': encode_jwt, 'id': user.pk})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)