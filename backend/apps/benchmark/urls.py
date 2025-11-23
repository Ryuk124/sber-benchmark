from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BankViewSet,
    ProductViewSet,
    CriterionViewSet,
    CompareAPIView,
    SnapshotListView,
    StatusAPIView,
)

app_name = 'benchmark'

router = DefaultRouter()
router.register(r'banks', BankViewSet, basename='bank')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'criteria', CriterionViewSet, basename='criterion')

urlpatterns = [
    path('', include(router.urls)),
    path('compare/', CompareAPIView.as_view(), name='compare'),
    path('snapshots/', SnapshotListView.as_view(), name='snapshots-list'),
    path('snapshots/<str:product_id>/', SnapshotListView.as_view(), name='snapshots-product'),
    path('status/', StatusAPIView.as_view(), name='status'),
]
