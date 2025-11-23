# SberBench Insights - Bank Benchmarking System

Полнофункциональная система для сбора, анализа и сравнения банковских продуктов и услуг.

## Архитектура

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React)                         │
│         http://localhost:5173 (Vite dev server)                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │ Backend API (Django + DRF)                              │  │
│   │ http://localhost:8000/api                               │  │
│   │                                                           │  │
│   │ ├─ GET /compare        → Сравнение банков              │  │
│   │ ├─ GET /banks          → Список банков                 │  │
│   │ ├─ GET /products       → Список продуктов              │  │
│   │ ├─ GET /criteria       → Список критериев              │  │
│   │ ├─ GET /snapshots      → История снимков               │  │
│   │ └─ GET /status         → Статус API                    │  │
│   └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │ Database (PostgreSQL)                                    │  │
│   │ localhost:5432                                            │  │
│   └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │ Cache & Broker (Redis)                                  │  │
│   │ localhost:6379                                            │  │
│   └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │ Background Tasks (Celery)                               │  │
│   │ ├─ Parser workers     → Сбор данных из источников      │  │
│   │ ├─ Scheduler (Beat)   → Периодический парсинг           │  │
│   │ └─ Cleanup tasks      → Архивирование старых данных     │  │
│   └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │ Metrics & Visualisation                                 │  │
│   │ ├─ InfluxDB          → Time-series metrics               │  │
│   │ └─ Grafana           → Dashboards (port 3000)            │  │
│   └──────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Быстрый старт (Docker Compose)

### 1. Предварительно
- Установите [Docker](https://www.docker.com/products/docker-desktop)
- Установите [Docker Compose](https://docs.docker.com/compose/install/)

### 2. Запуск всей системы

```bash
# Перейдите в папку backend
cd backend

# Скопируйте .env
cp .env.example .env

# Запустите все сервисы
docker-compose up -d

# Проверьте логи
docker-compose logs -f backend
```

### 3. Инициализация данных

```bash
# Выполнять автоматически при старте, но можно вручную:
docker-compose exec backend python manage.py init_data
docker-compose exec backend python manage.py migrate
```

### 4. Доступ к сервисам

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api
- **Django Admin**: http://localhost:8000/admin
- **Grafana**: http://localhost:3000 (admin/admin)
- **InfluxDB**: http://localhost:8086

### 5. Остановка

```bash
docker-compose down
```

---

## Локальный запуск (без Docker)

### Требования

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Node.js 18+ (для фронтенда)

### Backend Setup

```bash
cd backend

# Создайте virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Установите зависимости
pip install -r requirements.txt

# Скопируйте .env
cp .env.example .env

# Отредактируйте .env, установите DB credentials и SECRET_KEY

# Выполните миграции
python manage.py migrate

# Инициализируйте данные
python manage.py init_data

# Создайте superuser
python manage.py createsuperuser

# Запустите dev server
python manage.py runserver 0.0.0.0:8000
```

В отдельных терминалах запустите:

```bash
# Celery Worker
celery -A config worker --loglevel=info

# Celery Beat (scheduler)
celery -A config beat --loglevel=info
```

### Frontend Setup

```bash
cd /root

# Установите зависимости
npm install
# или
bun install

# Скопируйте .env
cp .env.example .env

# Запустите dev server (port 5173)
npm run dev
```

---

## API Endpoints

### Статус и информация

```bash
GET /api/status/
# Response: { status: "ok", timestamp, data: { banks, products, criteria, snapshots, sources } }
```

### Банки

```bash
GET /api/banks/
# Response: [{ id: "sber", name: "Сбербанк", website: "..." }, ...]

GET /api/banks/{id}/
# Response: { id: "sber", name: "Сбербанк", ... }
```

### Продукты

```bash
GET /api/products/
# Response: [{ id: "deposits", name: "Вклады", ... }, ...]
```

### Критерии

```bash
GET /api/criteria/
# Response: [{ id: "cost", name: "Стоимость обслуживания", ... }, ...]
```

### Сравнение банков (основной endpoint)

```bash
GET /api/compare/?banks=sber,vtb,alfa&criteria=cost,sms,interest&product=deposits

# Response:
{
  "date": "2025-11-22T12:00:00Z",
  "sources": [
    { "id": 1, "name": "Banki.ru", "url": "https://banki.ru" },
    { "id": 2, "name": "Sravni.ru", "url": "https://sravni.ru" }
  ],
  "data": {
    "sber": { "cost": true, "sms": false, "interest": true },
    "vtb": { "cost": false, "sms": true, "interest": true },
    "alfa": { "cost": true, "sms": true, "interest": false }
  },
  "confidence": {
    "sber.cost": 0.95,
    "vtb.sms": 0.87,
    "alfa.interest": 0.72
  },
  "is_mock": false,
  "note": "Data from 2025-11-22 12:00"
}
```

### История снимков

```bash
GET /api/snapshots/
GET /api/snapshots/{product_id}/
```

---

## Celery Tasks

### Парсинг данных продукта

```bash
# Через Django shell
from apps.tasks.celery_tasks import parse_product_data
parse_product_data.delay('deposits', 'mock')

# Или через celery CLI
celery -A config call apps.tasks.celery_tasks.parse_product_data --args '["deposits", "mock"]'
```

### Очистка старых снимков

```bash
celery -A config call apps.tasks.celery_tasks.cleanup_old_snapshots --args '[30]'
```

### Обновление метрик парсинга

```bash
celery -A config call apps.tasks.celery_tasks.update_parser_metrics
```

---

## Структура проекта

```
sberbench-insights-main/
├── backend/                      # Django backend
│   ├── config/                   # Django конфиг (settings, urls, wsgi, asgi)
│   ├── apps/
│   │   ├── benchmark/            # Основное приложение
│   │   │   ├── models.py         # DB models: Bank, Product, Criterion, Snapshot, FeatureValue, ParseLog
│   │   │   ├── views.py          # API endpoints
│   │   │   ├── serializers.py    # DRF serializers
│   │   │   ├── urls.py           # URL routing
│   │   │   ├── admin.py          # Django admin
│   │   │   └── management/
│   │   │       └── commands/
│   │   │           └── init_data.py  # Инициализация БД
│   │   ├── parsers/              # Parser модули
│   │   │   ├── base.py           # Базовый класс парсера
│   │   │   └── scrapers/         # Конкретные скрейперы
│   │   └── tasks/                # Celery задачи
│   │       └── celery_tasks.py
│   ├── manage.py
│   ├── requirements.txt
│   ├── docker-compose.yml        # Все сервисы
│   ├── Dockerfile                # Backend образ
│   └── README.md
│
├── src/                          # React frontend
│   ├── components/
│   │   ├── BankSelector.tsx      # Выбор банков
│   │   ├── ProductSelector.tsx   # Выбор продукта
│   │   ├── CriteriaSelector.tsx  # Выбор критериев
│   │   ├── ComparisonTable.tsx   # Таблица сравнения
│   │   ├── AIInsights.tsx        # AI анализ
│   │   ├── GrafanaPlaceholder.tsx # Grafana интеграция
│   │   └── ui/                   # shadcn/ui компоненты
│   ├── hooks/
│   │   ├── use-comparison-data.ts # Hook для API запросов
│   │   └── use-toast.ts
│   ├── pages/
│   │   ├── Index.tsx             # Главная страница
│   │   └── NotFound.tsx
│   ├── lib/
│   ├── App.tsx
│   └── main.tsx
│
├── package.json
├── vite.config.ts                # Proxy к backend
├── tailwind.config.ts
├── .env.example
└── README.md
```

---

## Дальнейшие шаги

### 1. Реализовать парсеры

Заполнить заготовки в `backend/apps/parsers/`:
- `BankiRuParser` для banki.ru
- `SravniRuParser` для sravni.ru
- `OfficialBankParser` для официальных сайтов банков
- Интеграция с RBK API

### 2. Настроить Grafana dashboards

- Подключить InfluxDB как datasource
- Создать дашборды для трендов процентных ставок
- Настроить алерты при изменении условий

### 3. Добавить AI-анализ

- Интеграция с LLM (OpenAI, Vertex AI, локальная модель)
- Генерация рекомендаций на основе данных
- Аналитика конкурентных преимуществ

### 4. Внедрить аутентификацию и авторизацию

- JWT токены для API
- Role-based access control (RBAC)
- Сохранение пользовательских отчётов

### 5. Production deployment

- Настроить SSL/TLS
- Использовать PostgreSQL backups
- Настроить CI/CD (GitHub Actions, GitLab CI)
- Добавить мониторинг (Sentry, ELK)

---

## Troubleshooting

### Backend не запускается

```bash
# Проверьте миграции
python manage.py migrate

# Проверьте зависимости
pip install -r requirements.txt --upgrade

# Посмотрите логи
python manage.py runserver --verbosity=2
```

### PostgreSQL connection error

```bash
# Убедитесь, что PostgreSQL запущен:
# Docker: docker-compose logs postgres
# Локально: brew services list | grep postgres

# Проверьте credentials в .env
```

### Celery tasks не выполняются

```bash
# Убедитесь, что Redis запущен
redis-cli ping

# Посмотрите логи worker'а
celery -A config worker --loglevel=debug

# Используйте Celery flower для мониторинга
pip install flower
celery -A config flower
```

### Frontend не подключается к API

```bash
# Проверьте CORS настройки в backend/config/settings.py
# Убедитесь, что backend запущен на http://localhost:8000
# Проверьте vite proxy в vite.config.ts
```

---

## Документация

- [Django](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery](https://docs.celeryproject.org/)
- [React](https://react.dev/)
- [Vite](https://vitejs.dev/)
- [Grafana](https://grafana.com/docs/)

---

## Лицензия

MIT

---

## Контакты и поддержка

Для вопросов и багов - создавайте issues в репозитории.
