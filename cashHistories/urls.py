from rest_framework.routers import DefaultRouter
from . import views


app_name = "cashHistories"


router = DefaultRouter()
router.register("", views.CashHistoryViewSet)
urlpatterns = router.urls