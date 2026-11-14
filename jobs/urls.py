from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobApplicationViewSet, AnalyzeView

router = DefaultRouter()
router.register(r"jobs", JobApplicationViewSet)

urlpatterns = [
    path("analyze/", AnalyzeView.as_view()),
    path("", include(router.urls)),
]