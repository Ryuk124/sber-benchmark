from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AIAnalysisViewSet, AIInsightsAPIView

app_name = 'ai'

router = DefaultRouter()
router.register(r'analysis', AIAnalysisViewSet, basename='analysis')

urlpatterns = [
    path('', include(router.urls)),
    path('insights/', AIInsightsAPIView.as_view(), name='insights'),
]
