# 🚀 Быстрый старт - sber-benchmark-main интеграция

## За 5 минут до запуска

### 1️⃣ Применить миграции (30 сек)
```bash
cd backend
python manage.py migrate apps.ai
```

### 2️⃣ Запустить backend (2 мин)
```bash
python manage.py runserver
```

Проверить: http://localhost:8000/api/ai/analysis/

### 3️⃣ Запустить frontend (1 мин)
```bash
# В отдельном терминале
npm run dev
```

Открыть: http://localhost:5173

---

## 🧪 Быстрые тесты

### Test 1: Проверить API
```bash
curl http://localhost:8000/api/ai/analysis/
# Должно вернуть: {"count": 0, "results": []}
```

### Test 2: Запустить анализ (Celery задача)
```bash
curl -X POST http://localhost:8000/api/ai/analysis/analyze/ \
  -H "Content-Type: application/json" \
  -d '{"competitor": "sber", "product": "deposits"}'
```

### Test 3: Получить insights
```bash
curl "http://localhost:8000/api/ai/insights/?banks=sber&product=deposits"
```

---

## 📊 Что появилось нового

| Компонент | Где | Статус |
|-----------|-----|--------|
| LLM Service | `apps/ai/llm_service.py` | ✅ Работает |
| Text Parser | `apps/ai/text_parser.py` | ✅ Готов |
| Celery Tasks | `apps/tasks/celery_tasks.py` | ✅ Готовы |
| API Endpoints | `apps/ai/views.py` | ✅ Работают |
| React Component | `AIInsights.tsx` | ✅ Обновлена |
| Admin Panel | Django admin | ✅ Добавлена |

---

## 🔌 Следующие шаги

### Для использования реальной LLM модели:

**Вариант 1: OpenAI GPT (ПРОЩЕ всего)** ✅
```bash
# 1. Установить пакет
pip install openai==1.3.0

# 2. Получить ключ: https://platform.openai.com/api-keys

# 3. Добавить в .env:
OPENAI_API_KEY=sk-proj-your-key-here

# 4. Готово! Система автоматически будет использовать GPT
```

**Вариант 2: Ollama (Локально, бесплатно)**
```bash
# 1. Установить Ollama с https://ollama.ai

# 2. Запустить в отдельном терминале:
ollama run llama2

# 3. Система автоматически подключится
```

**Полная документация**: см. `LLM_SETUP.md`

---

## 📈 Frontend интеграция

`AIInsights` компонент теперь:
- ✅ Загружает данные с backend при выборе банков/критериев
- ✅ Показывает реальные анализы
- ✅ Fallback на demo-данные если анализов нет
- ✅ Показывает статус загрузки

Используется в: `src/pages/Index.tsx`

```tsx
<AIInsights 
  banks={selectedBanks}
  criteria={selectedCriteria}
  product={selectedProduct}
/>
```

---

## 🎯 Production использование

### Автоматизация парсинга:

```python
# schedule_analysis.py
from apps.ai.text_parser import PageTextParser
from apps.ai.llm_service import LLMService

banks_data = {
    "sber": ["https://sberbank.ru/deposits", "..."],
    "vtb": ["https://vtb.ru/deposits", "..."],
}

for bank, urls in banks_data.items():
    parser = PageTextParser(bank, "deposits", "general", urls)
    pages = parser.run()
    
    llm = LLMService()
    results = llm.analyze_and_store(pages)
    
    print(f"Analyzed {len(results)} pages for {bank}")
```

### Запустить периодически (Celery Beat):

```python
# config/settings.py
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'daily-analysis': {
        'task': 'apps.tasks.celery_tasks.analyze_with_llm',
        'schedule': crontab(hour=2, minute=0),  # 02:00 UTC
        'args': ('sber', 'deposits')
    }
}
```

---

## ✅ Checklist

- [ ] Миграции применены (`python manage.py migrate apps.ai`)
- [ ] Backend запущен (`python manage.py runserver`)
- [ ] Frontend запущен (`npm run dev`)
- [ ] API endpoints доступны (`curl http://localhost:8000/api/ai/analysis/`)
- [ ] React компонент показывает данные
- [ ] Celery worker запущен (опционально для демо)

---

## 🐛 Troubleshooting

| Проблема | Решение |
|----------|---------|
| ModuleNotFoundError: apps.ai | Добавлена ли в INSTALLED_APPS? (`settings.py`) |
| Migration не работает | `python manage.py makemigrations apps.ai` |
| API 404 | Проверить urls.py - добавлена ли `path('api/ai/', include('apps.ai.urls'))` |
| React не загружает данные | Проверить browser console (F12), proxy работает? |
| Celery error | Redis запущен? `redis-cli ping` → должен вывести PONG |

---

**Все готово! 🎉 Начинайте разработку!**

Больше информации в:
- 📄 `SBER_BENCHMARK_INTEGRATION.md` - Обзор интеграции
- 📄 `AI_INTEGRATION.md` - Детальное руководство
