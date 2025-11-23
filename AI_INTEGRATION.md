# Интеграция sber-benchmark-main

## 📊 Что было интегрировано

Из проекта `sber-benchmark-main` в основной проект были перенесены:

### 1. **LLM Service** (`apps/ai/llm_service.py`)
Сервис для анализа банковских данных с использованием AI моделей.

**Возможности:**
- Хранение результатов анализа в БД (`AIAnalysisResult`)
- Поддержка разных типов анализа: facts, comparison, recommendation
- Управление confidence scores для каждого результата
- История анализов с метаданными (модель LLM, версия prompt)

**Интеграция с Django:**
```python
from apps.ai.llm_service import LLMService

llm_service = LLMService(llm_model="Qwen-14B", prompt_version="v1")
recommendations = llm_service.get_recommendations(bank_id="sber", product_id="deposits")
```

### 2. **Text Parser** (`apps/ai/text_parser.py`)
Парсер для скачивания и очистки текста со страниц.

**Возможности:**
- Загрузка HTML с сайтов
- Удаление скриптов, стилей и ненужного контента
- Очистка текста для анализа LLM
- Обработка ошибок при парсинге

**Использование:**
```python
from apps.ai.text_parser import PageTextParser

parser = PageTextParser(
    competitor="sber",
    product="deposits",
    criterion="cost",
    urls=["https://example.com/page1", "https://example.com/page2"]
)

results = parser.run()
# Возвращает список объектов с очищенным текстом
```

### 3. **Celery Tasks** (`apps/tasks/celery_tasks.py`)
Фоновые задачи для анализа:

- **`analyze_with_llm`** - запуск анализа для банка/продукта
- **`get_ai_recommendations`** - получение рекомендаций

**Использование:**
```python
from apps.tasks.celery_tasks import analyze_with_llm

# Запустить анализ в фоне
task = analyze_with_llm.delay(
    bank_id="sber",
    product_id="deposits",
    urls=["url1", "url2"]
)

# Проверить статус
print(task.status)
```

### 4. **API Endpoints** (`apps/ai/urls.py`, `apps/ai/views.py`)
REST API для взаимодействия с AI сервисом:

#### **GET /api/ai/analysis/**
Список всех анализов
```bash
curl "http://localhost:8000/api/ai/analysis/?competitor=sber&product=deposits"
```

#### **GET /api/ai/analysis/recommendations/**
Получить рекомендации
```bash
curl "http://localhost:8000/api/ai/analysis/recommendations/?competitor=sber&limit=10"
```

#### **POST /api/ai/analysis/analyze/**
Запустить анализ (запускает Celery задачу)
```bash
curl -X POST http://localhost:8000/api/ai/analysis/analyze/ \
  -H "Content-Type: application/json" \
  -d '{
    "competitor": "sber",
    "product": "deposits",
    "urls": ["url1", "url2"]
  }'
```

#### **GET /api/ai/insights/**
Получить AI insights по сравнению
```bash
curl "http://localhost:8000/api/ai/insights/?banks=sber,vtb&product=deposits&criterion=cost"
```

### 5. **React Component Updates**
`AIInsights.tsx` теперь загружает данные с backend:
- Отправляет запрос к `/api/ai/insights/`
- Отображает реальные анализы если есть
- Возвращает к demo-данным если анализов нет

## 🔧 Требуемые зависимости

Уже установлены в `requirements.txt`:
- `requests` - для скачивания HTML
- `beautifulsoup4` - для парсинга HTML

Если нужны:
- `qwen-api` - для интеграции с Qwen LLM
- `openai` - для интеграции с GPT

## 📝 Миграция БД

Создан новый app `apps/ai` с моделью `AIAnalysisResult`.

Для применения миграций:
```bash
python manage.py migrate apps.ai
```

## 🚀 Использование в production

### Запуск анализа для всех банков/продуктов:

```python
from apps.ai.text_parser import PageTextParser
from apps.ai.llm_service import LLMService

# Получить списки URL для каждого банка
bank_urls = {
    "sber": ["https://sberbank.ru/...", "..."],
    "vtb": ["https://vtb.ru/...", "..."],
    "alfa": ["https://alfabank.ru/...", "..."],
}

for bank, urls in bank_urls.items():
    parser = PageTextParser(
        competitor=bank,
        product="deposits",
        criterion="general",
        urls=urls
    )
    pages = parser.run()
    
    llm_service = LLMService()
    results = llm_service.analyze_and_store(pages, bank_id=bank)
```

### Автоматизация с Celery Beat:

Добавить в `config/settings.py`:
```python
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'analyze-banks-daily': {
        'task': 'apps.tasks.celery_tasks.analyze_with_llm',
        'schedule': crontab(hour=0, minute=0),  # Каждый день в 00:00
        'args': ('sber', 'deposits')
    },
}
```

## 📊 Модель данных

```
AIAnalysisResult
├── competitor (CharField) - название конкурента (банка)
├── product (CharField) - тип продукта
├── criterion (CharField) - критерий сравнения
├── analysis_type (CharField) - facts/comparison/recommendation
├── value (TextField) - результат анализа
├── source_url (URLField) - откуда взяты данные
├── confidence_score (FloatField) - уверенность результата (0-1)
├── llm_model (CharField) - какая модель использована
├── llm_prompt_version (CharField) - версия prompt'а
└── parsed_at/analysis_at (DateTimeField) - времени парсинга/анализа
```

## 🔌 Интеграция с LLM моделями

На данный момент используется mock LLM (`_run_llm_analysis` возвращает фиксированные данные).

Для реальной интеграции замените `_run_llm_analysis` в `llm_service.py`:

### Qwen (Alibaba)
```python
def _run_llm_analysis(self, text: str, ...):
    from qwen import QwenAPI
    
    client = QwenAPI(api_key=os.getenv("QWEN_API_KEY"))
    response = client.analyze_text(text, prompt=...)
    return response
```

### OpenAI GPT
```python
def _run_llm_analysis(self, text: str, ...):
    import openai
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": text}]
    )
    return response["choices"][0]["message"]["content"]
```

### Claude (Anthropic)
```python
def _run_llm_analysis(self, text: str, ...):
    import anthropic
    
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[{"role": "user", "content": text}]
    )
    return message.content[0].text
```

## 🧪 Тестирование

### Запустить анализ вручную:
```bash
python manage.py shell
```

```python
from apps.ai.text_parser import PageTextParser
from apps.ai.llm_service import LLMService

# Тест парсера
parser = PageTextParser("sber", "deposits", "cost", ["https://example.com"])
pages = parser.run()
print(f"Parsed {len(pages)} pages")

# Тест LLM сервиса
llm = LLMService()
results = llm.analyze_and_store(pages)
print(f"Analysis results: {len(results)}")
```

### Запустить Celery задачу:
```bash
# Terminal 1: Celery worker
celery -A config worker --loglevel=info

# Terminal 2: Запустить задачу
python manage.py shell
```

```python
from apps.tasks.celery_tasks import analyze_with_llm

task = analyze_with_llm.delay("sber", "deposits")
print(f"Task ID: {task.id}")
print(f"Task Status: {task.status}")
print(f"Task Result: {task.result}")
```

## 📚 Файловая структура

```
backend/apps/ai/
├── __init__.py
├── admin.py              # Django admin интеграция
├── apps.py               # Конфиг приложения
├── views.py              # API Views
├── urls.py               # URL роутинг
├── llm_service.py        # LLM сервис + AIAnalysisResult модель
├── text_parser.py        # Text parsing
└── migrations/
    ├── __init__.py
    └── 0001_initial.py
```

## ✅ Готово!

LLM интеграция полностью интегрирована и готова к использованию. Для запуска:

```bash
# 1. Применить миграции
python manage.py migrate

# 2. Запустить backend
python manage.py runserver

# 3. Запустить Celery worker (опционально)
celery -A config worker

# 4. Запустить React
npm run dev

# 5. Открыть http://localhost:5173
```
