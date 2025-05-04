from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import StudentViewSet, SubjectViewSet, ScoreViewSet

router = DefaultRouter()
router.register('student', StudentViewSet)
router.register('subject', SubjectViewSet)
router.register('score', ScoreViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
