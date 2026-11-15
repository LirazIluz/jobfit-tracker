from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobApplicationViewSet, AnalyzeView
from .views import JobApplicationViewSet, AnalyzeView, AnalyzeAIView

router = DefaultRouter()
router.register(r"jobs", JobApplicationViewSet)

urlpatterns = [
    path("analyze/", AnalyzeView.as_view()),
    path("", include(router.urls)),
    path("analyze-ai/", AnalyzeAIView.as_view()),
]