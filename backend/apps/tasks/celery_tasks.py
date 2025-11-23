"""
Celery задачи для парсинга и обработки данных
"""

import logging
from celery import shared_task
from datetime import datetime
from apps.benchmark.models import Snapshot, Product, FeatureValue, Bank, Criterion, Source, ParseLog
from apps.parsers.base import MockParser

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def parse_product_data(self, product_id: str, parser_type: str = 'mock'):
    """
    Основная задача для парсинга данных продукта.
    
    Args:
        product_id: ID продукта (e.g., 'deposits', 'credits')
        parser_type: тип парсера ('mock', 'banki_ru', 'sravni_ru', 'official', etc.)
    
    Returns:
        dict: результат парсинга
    """
    try:
        logger.info(f'Starting parse_product_data for product={product_id}, parser={parser_type}')
        
        # Get or create product
        product, created = Product.objects.get_or_create(
            id=product_id,
            defaults={'name': product_id.replace('_', ' ').title()}
        )
        
        # Create snapshot
        snapshot = Snapshot.objects.create(
            product=product,
            parsing_status='in_progress',
            note=f'Parsing with {parser_type}'
        )
        
        try:
            # Initialize parser
            if parser_type == 'mock':
                parser = MockParser()
            else:
                # TODO: Add other parser types
                raise NotImplementedError(f'Parser type {parser_type} not implemented')
            
            # Get list of banks
            banks = list(Bank.objects.all())
            if not banks:
                logger.warning('No banks found in database. Add some banks to proceed.')
                snapshot.parsing_status = 'warning'
                snapshot.save()
                return {'status': 'warning', 'message': 'No banks in database'}
            
            # Parse data for each bank
            for bank in banks:
                try:
                    result = parser.parse(bank=bank.id, product=product_id)
                    
                    # Save criteria values
                    for criterion_id, crit_data in result.get('criteria', {}).items():
                        # Get or create criterion
                        criterion, _ = Criterion.objects.get_or_create(
                            id=criterion_id,
                            defaults={'name': criterion_id.replace('_', ' ').title()}
                        )
                        
                        # Get or create source (if provided)
                        source = None
                        if 'source_name' in crit_data:
                            source, _ = Source.objects.get_or_create(
                                name=crit_data['source_name'],
                                defaults={
                                    'url': crit_data.get('source_url', 'https://example.com')
                                }
                            )
                        
                        # Create/update feature value
                        FeatureValue.objects.update_or_create(
                            snapshot=snapshot,
                            bank=bank,
                            criterion=criterion,
                            defaults={
                                'value': crit_data.get('value', False),
                                'confidence': crit_data.get('confidence'),
                                'source': source,
                                'source_url': crit_data.get('source_url'),
                                'raw_data': crit_data,
                            }
                        )
                        
                        logger.debug(f'Saved {bank.id}/{criterion_id}: {crit_data["value"]}')
                    
                    # Log success
                    ParseLog.objects.create(
                        source=source or Source.objects.first(),
                        snapshot=snapshot,
                        status='success',
                        message=f'Successfully parsed {bank.name}'
                    )
                    
                except Exception as e:
                    logger.error(f'Error parsing {bank.id}: {str(e)}', exc_info=True)
                    ParseLog.objects.create(
                        source=Source.objects.first(),
                        snapshot=snapshot,
                        status='error',
                        message=f'Error parsing {bank.name}',
                        error_trace=str(e)
                    )
            
            # Mark snapshot as completed
            snapshot.parsing_status = 'completed'
            snapshot.save()
            
            logger.info(f'Completed parse_product_data for {product_id}')
            return {'status': 'success', 'snapshot_id': snapshot.id}
            
        except Exception as e:
            logger.error(f'Fatal error in parse_product_data: {str(e)}', exc_info=True)
            snapshot.parsing_status = 'failed'
            snapshot.save()
            raise
        
        finally:
            if 'parser' in locals():
                parser.close()
    
    except Exception as e:
        logger.error(f'Unexpected error in parse_product_data: {str(e)}', exc_info=True)
        raise


@shared_task
def cleanup_old_snapshots(days: int = 30):
    """
    Удаляет старые снимки (старше N дней).
    
    Args:
        days: количество дней для сохранения
    """
    from django.utils import timezone
    from datetime import timedelta
    
    cutoff_date = timezone.now() - timedelta(days=days)
    deleted_count, _ = Snapshot.objects.filter(
        created_at__lt=cutoff_date,
        is_active=False
    ).delete()
    
    logger.info(f'Cleaned up {deleted_count} old snapshots')
    return {'deleted': deleted_count}


@shared_task
def update_parser_metrics():
    """
    Обновляет метрики парсинга для мониторинга.
    TODO: Отправить метрики в Prometheus/Grafana
    """
    from django.db.models import Count
    
    metrics = {
        'total_snapshots': Snapshot.objects.count(),
        'active_snapshots': Snapshot.objects.filter(is_active=True).count(),
        'failed_snapshots': Snapshot.objects.filter(parsing_status='failed').count(),
        'total_features': FeatureValue.objects.count(),
        'error_logs': ParseLog.objects.filter(status='error').count(),
    }
    
    logger.info(f'Parser metrics: {metrics}')
    # TODO: Send to Prometheus
    return metrics


@shared_task(bind=True)
def analyze_with_llm(self, bank_id: str, product_id: str, urls: list = None):
    """
    Запускает анализ данных банка с использованием LLM.
    
    Args:
        bank_id: ID банка для анализа
        product_id: ID продукта
        urls: Список URL для парсинга (опционально)
    
    Returns:
        dict: Результаты анализа
    """
    try:
        from apps.ai.text_parser import PageTextParser
        from apps.ai.llm_service import LLMService
        
        logger.info(f'Starting LLM analysis for {bank_id}/{product_id}')
        
        # Если нет URLs, используем mock данные
        if not urls:
            urls = [
                f"https://example.com/{bank_id}/{product_id}/page1",
                f"https://example.com/{bank_id}/{product_id}/page2",
            ]
        
        # Шаг 1: Парсим текст со страниц
        parser = PageTextParser(
            competitor=bank_id,
            product=product_id,
            criterion="general",
            urls=urls
        )
        
        parsed_pages = parser.run()
        logger.info(f'Parsed {len(parsed_pages)} pages')
        
        # Шаг 2: Анализируем с LLM
        llm_service = LLMService(llm_model="Qwen-14B", prompt_version="v1")
        analysis_results = llm_service.analyze_and_store(
            pages=parsed_pages,
            bank_id=bank_id,
            product_id=product_id
        )
        
        logger.info(f'Completed LLM analysis: {len(analysis_results)} results')
        
        return {
            'status': 'success',
            'bank_id': bank_id,
            'product_id': product_id,
            'analyzed_pages': len(analysis_results),
            'results': [r.get('source_url', '') for r in analysis_results if 'error' not in r]
        }
        
    except Exception as e:
        logger.error(f'Error in analyze_with_llm: {str(e)}', exc_info=True)
        return {
            'status': 'error',
            'bank_id': bank_id,
            'product_id': product_id,
            'error': str(e)
        }


@shared_task
def get_ai_recommendations(bank_id: str = None, product_id: str = None):
    """
    Получить AI рекомендации на основе анализа.
    
    Args:
        bank_id: ID банка (опционально)
        product_id: ID продукта (опционально)
    
    Returns:
        list: Список рекомендаций
    """
    try:
        from apps.ai.llm_service import LLMService
        
        llm_service = LLMService()
        recommendations = llm_service.get_recommendations(
            bank_id=bank_id,
            product_id=product_id,
            limit=10
        )
        
        logger.info(f'Retrieved {len(recommendations)} recommendations')
        return recommendations
        
    except Exception as e:
        logger.error(f'Error in get_ai_recommendations: {str(e)}', exc_info=True)
        return []
