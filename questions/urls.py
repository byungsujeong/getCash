from rest_framework.routers import DefaultRouter

from . import views


app_name = "questions"

router = DefaultRouter()
router.register("", views.QuestionViewSet)
urlpatterns = router.urls
