"""
API Views для AI анализа
"""

import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from apps.ai.llm_service import AIAnalysisResult, LLMService
from apps.benchmark.serializers import AIAnalysisResultSerializer

logger = logging.getLogger(__name__)


class AIAnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра результатов AI анализа.
    
    GET /api/ai/analysis/ - список анализов
    GET /api/ai/analysis/{id}/ - детали анализа
    GET /api/ai/analysis/recommendations/ - получить рекомендации
    """
    
    queryset = AIAnalysisResult.objects.all()
    serializer_class = AIAnalysisResultSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['competitor', 'product', 'criterion', 'analysis_type']
    ordering = ['-analysis_at']
    
    @action(detail=False, methods=['get'])
    def recommendations(self, request):
        """
        Получить AI рекомендации.
        
        Query params:
        - competitor: название конкурента (опционально)
        - product: тип продукта (опционально)
        - limit: максимум рекомендаций (по умолчанию 10)
        """
        try:
            competitor = request.query_params.get('competitor')
            product = request.query_params.get('product')
            limit = int(request.query_params.get('limit', 10))
            
            llm_service = LLMService()
            recommendations = llm_service.get_recommendations(
                bank_id=competitor,
                product_id=product,
                limit=limit
            )
            
            return Response({
                'status': 'success',
                'count': len(recommendations),
                'recommendations': recommendations
            })
        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def analyze(self, request):
        """
        Запустить анализ для конкретного банка/продукта.
        
        POST /api/ai/analysis/analyze/
        
        Body:
        {
            "competitor": "sber",
            "product": "deposits",
            "urls": ["url1", "url2"]  // опционально
        }
        """
        try:
            competitor = request.data.get('competitor')
            product = request.data.get('product')
            urls = request.data.get('urls', [])
            
            if not competitor or not product:
                return Response(
                    {'error': 'Missing competitor or product'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Запускаем задачу в Celery
            from apps.tasks.celery_tasks import analyze_with_llm
            task = analyze_with_llm.delay(competitor, product, urls)
            
            return Response({
                'status': 'started',
                'task_id': task.id,
                'competitor': competitor,
                'product': product
            })
        except Exception as e:
            logger.error(f"Error starting analysis: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AIInsightsAPIView(APIView):
    """
    Endpoint для получения AI insights по сравнению банков.
    
    GET /api/ai/insights/?banks=sber,vtb&product=deposits&criterion=cost
    """
    
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Получить insights по сравнению"""
        try:
            banks = request.query_params.get('banks', '').split(',')
            product = request.query_params.get('product', 'deposits')
            criterion = request.query_params.get('criterion', '')
            
            # Получаем анализы из БД
            queryset = AIAnalysisResult.objects.filter(
                analysis_type__in=['facts', 'comparison']
            )
            
            if banks and banks[0]:
                queryset = queryset.filter(competitor__in=banks)
            
            if product:
                queryset = queryset.filter(product=product)
            
            if criterion:
                queryset = queryset.filter(criterion=criterion)
            
            insights = AIAnalysisResultSerializer(queryset[:20], many=True).data
            
            return Response({
                'status': 'success',
                'count': len(insights),
                'banks': banks,
                'product': product,
                'criterion': criterion,
                'insights': insights
            })
        except Exception as e:
            logger.error(f"Error getting insights: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
