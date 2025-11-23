"""
LLM Service для анализа данных банков с использованием AI модели.
Интегрируется с PageTextParser для обработки данных и хранит результаты в БД.
"""

from datetime import datetime
from typing import List, Dict, Optional
import logging
import json

from django.db import models
from apps.benchmark.models import Source, FeatureValue, Bank, Criterion, Snapshot, Product

logger = logging.getLogger(__name__)


class AIAnalysisResult(models.Model):
    """Модель для хранения результатов AI анализа"""
    
    ANALYSIS_TYPES = [
        ('facts', 'Extraction of Facts'),
        ('comparison', 'Comparison Analysis'),
        ('recommendation', 'Recommendation'),
    ]
    
    competitor = models.CharField(max_length=200, db_index=True)
    product = models.CharField(max_length=200)
    criterion = models.CharField(max_length=200)
    analysis_type = models.CharField(max_length=20, choices=ANALYSIS_TYPES, default='facts')
    value = models.TextField(null=True, blank=True)
    source_url = models.URLField(null=True, blank=True)
    parsed_at = models.DateTimeField()
    analysis_at = models.DateTimeField(auto_now_add=True)
    llm_model = models.CharField(max_length=100, default="Qwen-14B")
    llm_prompt_version = models.CharField(max_length=50, default="v1")
    confidence_score = models.FloatField(null=True, blank=True)
    raw_response = models.JSONField(null=True, blank=True)
    
    class Meta:
        ordering = ['-analysis_at']
        indexes = [
            models.Index(fields=['competitor', 'product']),
            models.Index(fields=['parsed_at']),
        ]
    
    def __str__(self):
        return f"{self.competitor} - {self.product} - {self.criterion}"


class LLMService:
    """
    Сервис для анализа данных с помощью LLM.
    
    Функциональность:
    - Прием результатов от PageTextParser
    - Отправка текста на анализ в LLM модель
    - Сохранение результатов в БД
    - Синхронизация с основной моделью данных
    """
    
    def __init__(self, llm_model: str = "Qwen-14B", prompt_version: str = "v1"):
        self.llm_model = llm_model
        self.prompt_version = prompt_version
        self.llm_provider = self._init_llm_provider()
    
    def _init_llm_provider(self):
        """Инициализация LLM провайдера (заглушка для демо)"""
        # TODO: Подключить реальную LLM модель (Qwen, GPT, Claude и т.д.)
        return None
    
    def analyze_and_store(
        self,
        pages: List[Dict],
        bank_id: str = None,
        product_id: str = None,
        time_override: Optional[datetime] = None
    ) -> List[Dict]:
        """
        Анализируем список страниц и сохраняем результаты.
        
        Args:
            pages: Список объектов от PageTextParser
            bank_id: ID банка (опционально)
            product_id: ID продукта (опционально)
            time_override: Переопределить время анализа
            
        Returns:
            Список результатов анализа
        """
        results = []
        
        for page in pages:
            if 'error' in page:
                logger.warning(f"Skipping page with error: {page['error']}")
                continue
            
            if not page.get("cleaned_text"):
                logger.warning(f"Skipping page without cleaned_text: {page.get('source_url')}")
                continue
            
            try:
                # Проводим анализ текста
                analysis = self._run_llm_analysis(
                    text=page["cleaned_text"],
                    competitor=page.get("competitor"),
                    product=page.get("product"),
                    criterion=page.get("criterion"),
                )
                
                parsed_at = datetime.fromisoformat(
                    page.get("parsed_at", datetime.utcnow().isoformat())
                )
                time_value = time_override if time_override else parsed_at
                
                # Сохраняем результат в БД
                record = {
                    **analysis,
                    "source_url": page.get("source_url"),
                    "parsed_at": parsed_at,
                    "time": time_value,
                    "llm_model": self.llm_model,
                    "llm_prompt_version": self.prompt_version
                }
                
                self._insert_record(record)
                results.append(record)
                
            except Exception as e:
                logger.error(f"Error analyzing page {page.get('source_url')}: {e}")
                results.append({
                    "source_url": page.get("source_url"),
                    "error": str(e)
                })
        
        return results
    
    def _run_llm_analysis(
        self,
        text: str,
        competitor: str = None,
        product: str = None,
        criterion: str = None
    ) -> Dict:
        """
        Запускаем LLM анализ текста.
        
        Поддерживает:
        - OpenAI GPT (требует OPENAI_API_KEY в .env)
        - Локальные mock данные (по умолчанию для демо)
        
        Для использования OpenAI GPT:
        1. pip install openai
        2. Добавить в .env: OPENAI_API_KEY=sk-...
        """
        
        # Попробуем использовать OpenAI если доступен
        try:
            import os
            api_key = os.getenv('OPENAI_API_KEY')
            
            if api_key and api_key != 'your_key_here':
                return self._analyze_with_openai(
                    text=text,
                    competitor=competitor,
                    product=product,
                    criterion=criterion,
                    api_key=api_key
                )
        except ImportError:
            logger.info("OpenAI not installed, using mock analysis")
        except Exception as e:
            logger.warning(f"OpenAI analysis failed: {e}, falling back to mock")
        
        # Fallback на mock анализ для демонстрации
        return self._analyze_with_mock(
            text=text,
            competitor=competitor,
            product=product,
            criterion=criterion
        )
    
    def _analyze_with_openai(
        self,
        text: str,
        competitor: str,
        product: str,
        criterion: str,
        api_key: str
    ) -> Dict:
        """Анализ с использованием OpenAI GPT"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=api_key)
            
            prompt = f"""
            Проанализируй текст о банковском продукте и извлеки ключевую информацию.
            
            Конкурент: {competitor}
            Продукт: {product}
            Критерий: {criterion}
            
            Текст:
            {text[:2000]}
            
            Ответь в формате JSON:
            {{
                "fact": "основной факт из текста",
                "value": "конкретное значение если есть",
                "confidence": 0.0-1.0
            }}
            """
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты эксперт по банковским продуктам"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            # Парсим ответ
            import json
            response_text = response.choices[0].message.content
            
            try:
                data = json.loads(response_text)
                return {
                    "competitor": competitor,
                    "product": product,
                    "criterion": criterion,
                    "value": data.get("fact", response_text),
                    "analysis_type": "facts",
                    "confidence_score": data.get("confidence", 0.75),
                    "llm_provider": "openai"
                }
            except json.JSONDecodeError:
                return {
                    "competitor": competitor,
                    "product": product,
                    "criterion": criterion,
                    "value": response_text,
                    "analysis_type": "facts",
                    "confidence_score": 0.7,
                    "llm_provider": "openai"
                }
                
        except Exception as e:
            logger.error(f"OpenAI analysis error: {e}")
            raise
    
    def _analyze_with_mock(
        self,
        text: str,
        competitor: str,
        product: str,
        criterion: str
    ) -> Dict:
        """Mock анализ для демонстрации без API ключа"""
        import random
        
        # Генерируем реалистичный mock-анализ
        mock_facts = {
            ("sber", "deposits"): [
                "Процент на остаток составляет 3.5% годовых",
                "Минимальная сумма вклада - 10 тысяч рублей",
                "Возможность снятия без комиссии",
            ],
            ("vtb", "deposits"): [
                "Ставка до 4.2% годовых",
                "Минимум - 5 тысяч рублей",
                "Автопродление вклада",
            ],
            ("alfa", "credits"): [
                "Кредитная ставка от 7.9% годовых",
                "Максимальный лимит - 5 млн рублей",
                "Срок одобрения - до 5 минут",
            ],
        }
        
        key = (competitor, product)
        facts = mock_facts.get(key, [
            f"Анализ {competitor} по {product}: стандартные условия",
            f"Предложение конкурентно по рынку",
        ])
        
        return {
            "competitor": competitor,
            "product": product,
            "criterion": criterion,
            "value": random.choice(facts),
            "analysis_type": "facts",
            "confidence_score": random.uniform(0.6, 0.95),
            "llm_provider": "mock"
        }
    
    def _insert_record(self, record: Dict):
        """Сохраняем результат анализа в БД"""
        try:
            analysis = AIAnalysisResult.objects.create(
                competitor=record.get("competitor"),
                product=record.get("product"),
                criterion=record.get("criterion"),
                analysis_type=record.get("analysis_type", "facts"),
                value=record.get("value"),
                source_url=record.get("source_url"),
                parsed_at=record.get("parsed_at", datetime.utcnow()),
                llm_model=record.get("llm_model", self.llm_model),
                llm_prompt_version=record.get("llm_prompt_version", self.prompt_version),
                confidence_score=record.get("confidence_score"),
                raw_response=record
            )
            logger.info(f"Stored analysis result: {analysis.id}")
            return analysis
        except Exception as e:
            logger.error(f"Error storing analysis result: {e}")
            raise
    
    def get_recommendations(
        self,
        bank_id: str = None,
        product_id: str = None,
        limit: int = 5
    ) -> List[Dict]:
        """
        Получить рекомендации на основе сохраненных анализов.
        
        Args:
            bank_id: Фильтр по банку
            product_id: Фильтр по продукту
            limit: Максимум результатов
            
        Returns:
            Список рекомендаций
        """
        queryset = AIAnalysisResult.objects.filter(
            analysis_type='recommendation'
        ).order_by('-analysis_at')[:limit]
        
        return [
            {
                "competitor": r.competitor,
                "product": r.product,
                "criterion": r.criterion,
                "recommendation": r.value,
                "confidence": r.confidence_score,
            }
            for r in queryset
        ]
