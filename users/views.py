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
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
        except Exception as e:
            return Response(data={'code':400, 'message': e, 'data':None})
        return Response(data={'code':0, 'message': None, 'data':serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except Exception as e:
            return Response(data={'code':400, 'message': e, 'data':None})
        return Response(data={'code':0, 'message': None, 'data':serializer.data})

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Exception as e:
            return Response(data={'code':400, 'message': e, 'data':None})
        return Response(data={'code':0, 'message': None, 'data':None}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(data={'code':400, 'message': 'bad request', 'data':None}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            encode_jwt = jwt.encode({"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256")
            return Response(data={'code':0, 'message': None, 'data':{'token': encode_jwt, 'id': user.pk}})
        else:
            return Response(data={'code':401, 'message': 'unauthorized', 'data':None}, status=status.HTTP_401_UNAUTHORIZED)