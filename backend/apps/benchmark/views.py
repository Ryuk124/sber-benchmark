import logging
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from django.db.models import Q
from .models import Bank, Product, Criterion, Snapshot, FeatureValue, Source
from .serializers import (
    BankSerializer,
    ProductSerializer,
    CriterionSerializer,
    SnapshotSerializer,
    ComparisonDataSerializer,
)

logger = logging.getLogger(__name__)


class BankViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для получения списка банков"""
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для получения списка продуктов"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class CriterionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для получения списка критериев"""
    queryset = Criterion.objects.all()
    serializer_class = CriterionSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class CompareAPIView(APIView):
    """
    API endpoint для получения сравнения банков по критериям.
    
    Query Parameters:
    - banks: список ID банков через запятую (например: sber,vtb,alfa)
    - criteria: список ID критериев через запятую
    - product: ID продукта
    
    Example:
    GET /api/compare?banks=sber,vtb&criteria=cost,sms&product=deposits
    """
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            # Parse query parameters
            banks_param = request.query_params.get('banks', 'sber').split(',')
            criteria_param = request.query_params.get('criteria', '').split(',')
            product_id = request.query_params.get('product', 'deposits')

            # Filter out empty strings
            banks_param = [b.strip() for b in banks_param if b.strip()]
            criteria_param = [c.strip() for c in criteria_param if c.strip()]

            # Get latest snapshot for product
            try:
                product = Product.objects.get(id=product_id)
                snapshot = product.snapshots.filter(is_active=True).latest('created_at')
            except Product.DoesNotExist:
                logger.warning(f'Product {product_id} not found')
                # Return mock data if product doesn't exist (for development)
                return Response(self._get_mock_data(banks_param, criteria_param))
            except Snapshot.DoesNotExist:
                logger.warning(f'No active snapshot for product {product_id}')
                # Return mock data if snapshot doesn't exist
                return Response(self._get_mock_data(banks_param, criteria_param))

            # Build comparison data
            data = {}
            sources_set = set()
            confidence_data = {}

            for bank_id in banks_param:
                data[bank_id] = {}
                for criterion_id in criteria_param:
                    try:
                        fv = snapshot.features.select_related('source').get(
                            bank_id=bank_id,
                            criterion_id=criterion_id
                        )
                        data[bank_id][criterion_id] = fv.value
                        if fv.confidence:
                            confidence_data[f'{bank_id}.{criterion_id}'] = fv.confidence
                        if fv.source:
                            sources_set.add(fv.source.id)
                    except FeatureValue.DoesNotExist:
                        data[bank_id][criterion_id] = False

            # Get unique sources
            sources = list(Source.objects.filter(id__in=sources_set).values('id', 'name', 'url'))

            response_data = {
                'date': snapshot.created_at.isoformat(),
                'sources': sources,
                'data': data,
                'confidence': confidence_data,
                'note': snapshot.note or f'Data from {snapshot.created_at.strftime("%Y-%m-%d %H:%M")}',
                'product': product_id,
                'is_mock': False,
            }

            return Response(response_data)

        except Exception as e:
            logger.error(f'Error in CompareAPIView: {str(e)}', exc_info=True)
            return Response(
                {'error': 'Internal server error', 'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _get_mock_data(self, banks, criteria):
        """Генерирует mock-данные для демо"""
        import random
        
        data = {}
        for bank_id in banks:
            data[bank_id] = {}
            for criterion_id in criteria:
                # Sber has slightly better chances for demo
                chance = 0.75 if bank_id == 'sber' else 0.6
                data[bank_id][criterion_id] = random.random() > chance

        return {
            'date': datetime.now().isoformat(),
            'sources': [
                {'id': 1, 'name': 'Banki.ru', 'url': 'https://banki.ru'},
                {'id': 2, 'name': 'Sravni.ru', 'url': 'https://sravni.ru'},
            ],
            'data': data,
            'confidence': {},
            'note': 'Mock data for demonstration (no real data available)',
            'product': 'deposits',
            'is_mock': True,
        }


class SnapshotListView(APIView):
    """Получить список снимков для продукта"""
    permission_classes = [AllowAny]

    def get(self, request, product_id=None):
        queryset = Snapshot.objects.select_related('product').all()
        
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        
        snapshots = queryset[:10]  # Last 10 snapshots
        serializer = SnapshotSerializer(snapshots, many=True)
        
        return Response({
            'count': len(snapshots),
            'results': serializer.data
        })


class StatusAPIView(APIView):
    """Проверить статус API и доступных данных"""
    permission_classes = [AllowAny]

    def get(self, request):
        banks_count = Bank.objects.count()
        products_count = Product.objects.count()
        criteria_count = Criterion.objects.count()
        snapshots_count = Snapshot.objects.count()
        sources_count = Source.objects.count()

        return Response({
            'status': 'ok',
            'timestamp': datetime.now().isoformat(),
            'data': {
                'banks': banks_count,
                'products': products_count,
                'criteria': criteria_count,
                'snapshots': snapshots_count,
                'sources': sources_count,
            },
            'message': 'API is running',
        })
