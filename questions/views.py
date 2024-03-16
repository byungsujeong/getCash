from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated

from .serializers import QuestionSerializer
from .permissions import IsSelf
from .models import Question


# Create your views here.
class QuestionViewSet(ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

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
