# SberBench Insights - Bank Benchmarking System

🏦 Интеллектуальная система для сбора, анализа и сравнения банковских продуктов и услуг

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![React 18+](https://img.shields.io/badge/React-18%2B-61dafb)](https://react.dev/)
[![Django 4.2+](https://img.shields.io/badge/Django-4.2%2B-092E20)](https://www.djangoproject.com/)
[![AI-Powered](https://img.shields.io/badge/AI--Powered-LLM-purple)](https://github.com)

## 📋 Описание

**SberBench Insights** - это MVP решение для Сбербанка, которое позволяет:

- ✅ Собирать данные о банковских продуктах из открытых источников (banki.ru, sravni.ru, frankrg.com, RBK)
- ✅ Консолидировать данные в единой системе с версионированием по датам
- ✅ Сравнивать условия Сбера с конкурентами (ВТБ, Альфа-Банк и др.)
- ✅ Генерировать аналитические отчёты и рекомендации по улучшению с использованием AI/LLM
- ✅ Визуализировать тренды и метрики через Grafana дашборды

## 🏗️ Архитектура

Система разделена на три части:

### Frontend (React + Vite + TypeScript)
- **Порт**: 5173
- **Задача**: UI для выбора банков, продуктов, критериев и просмотра результатов
- **Компоненты**: BankSelector, ProductSelector, CriteriaSelector, ComparisonTable, AIInsights, GrafanaPlaceholder

### Backend (Django + DRF + Celery)
- **Порт**: 8000
- **Задача**: API endpoints, обработка запросов, управление данными
- **Основные endpoints**: 
  - `/api/compare/` - сравнение банков
  - `/api/banks/` - список банков
  - `/api/products/` - список продуктов
  - `/api/criteria/` - список критериев
  - `/api/ai/analysis/` - AI анализы
  - `/api/ai/insights/` - AI insights по сравнению

### Infrastructure & AI
- **PostgreSQL**: Основная база данных (порт 5432)
- **Redis**: Кэш и Celery broker (порт 6379)
- **Celery Worker**: Фоновые задачи парсинга и анализа
- **Celery Beat**: Планировщик для периодического парсинга
- **InfluxDB**: Time-series база для метрик (порт 8086)
- **Grafana**: Визуализация дашбордов (порт 3000)
- **LLM Service**: AI-анализ данных (интеграция с Qwen/GPT/Claude)

## 🚀 Быстрый старт (Docker Compose)

### Требования
- Docker & Docker Compose
- 8GB RAM
- 5GB свободного места на диске

### Установка и запускbash
# Перейдите в папку backend
cd backend

# Скопируйте конфиг
cp .env.example .env

# Запустите все сервисы (первый запуск ~ 2-3 минуты)
docker-compose up -d

# Проверьте статус
docker-compose ps
```

### Доступ к сервисам

После запуска откройте в браузере:

| Сервис | URL | Учётные данные |
|--------|-----|----------------|
| **Frontend** | http://localhost:5173 | - |
| **Backend API** | http://localhost:8000/api | - |
| **Django Admin** | http://localhost:8000/admin | admin/admin |
| **Grafana** | http://localhost:3000 | admin/admin |

## 💻 Локальный запуск (без Docker)

### Backend

```bash
cd backend

# Создайте virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Установите зависимости
pip install -r requirements.txt

# Скопируйте .env и отредактируйте
cp .env.example .env
# Установите DB и Redis credentials

# Выполните миграции
python manage.py migrate

# Инициализируйте данные
python manage.py init_data

# Запустите dev server
python manage.py runserver 0.0.0.0:8000
```

В отдельных терминалах:

```bash
# Terminal 2: Celery Worker
celery -A config worker --loglevel=info

# Terminal 3: Celery Beat (scheduler)
celery -A config beat --loglevel=info
```

### Frontend

```bash
# Terminal 4
npm install
npm run dev
```

## 🔌 API Endpoints

### Сравнение банков (основной endpoint)

```bash
GET /api/compare/?banks=sber,vtb,alfa&criteria=cost,sms,interest&product=deposits

# Response example:
{
  "date": "2025-11-22T12:00:00Z",
  "sources": [
    {"name": "Banki.ru", "url": "https://banki.ru"},
    {"name": "Sravni.ru", "url": "https://sravni.ru"}
  ],
  "data": {
    "sber": {"cost": true, "sms": false, "interest": true},
    "vtb": {"cost": false, "sms": true, "interest": true},
    "alfa": {"cost": true, "sms": true, "interest": false}
  },
  "confidence": {
    "sber.cost": 0.95,
    "vtb.sms": 0.87
  },
  "is_mock": false
}
```

### Остальные endpoints

- `GET /api/banks/` - Список банков
- `GET /api/products/` - Список продуктов
- `GET /api/criteria/` - Список критериев
- `GET /api/snapshots/` - История снимков
- `GET /api/status/` - Статус API

Полная документация: см. [`backend/README.md`](backend/README.md)

## 📊 Структура проекта

```
sberbench-insights-main/
├── backend/                  # Django backend (основная логика)
│   ├── config/               # Django settings
│   ├── apps/
│   │   ├── benchmark/        # Основное приложение
│   │   ├── parsers/          # Парсеры (заготовки)
│   │   └── tasks/            # Celery задачи
│   ├── docker-compose.yml    # Все сервисы
│   └── README.md             # Подробная документация
│
├── src/                      # React frontend
│   ├── components/           # React компоненты
│   ├── hooks/                # Кастомные хуки (use-comparison-data)
│   └── pages/                # Страницы
│
├── public/                   # Статичные файлы
├── vite.config.ts            # Vite конфиг с proxy
└── FULL_SETUP.md             # Расширенная документация
```

## ⚙️ Конфигурация

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000
```

### Backend (.env)
```bash
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=sberbench
DB_USER=sberbench
DB_PASSWORD=sberbench
REDIS_URL=redis://localhost:6379/0
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

## 🔧 Дальнейшее развитие

### 1️⃣ Реализация парсеров (Priority: HIGH)
- [ ] Parser для banki.ru
- [ ] Parser для sravni.ru
- [ ] Parser для официальных сайтов банков
- [ ] Parser для RBK

### 2️⃣ AI Анализ (Priority: HIGH)
- [ ] Интеграция с LLM (OpenAI / Vertex AI)
- [ ] Генерация рекомендаций
- [ ] Аналитика конкурентных преимуществ

### 3️⃣ Grafana Dashboards (Priority: MEDIUM)
- [ ] Тренды процентных ставок
- [ ] Сравнительные heat maps
- [ ] Корреляционный анализ
- [ ] Алерты при изменениях

### 4️⃣ Аутентификация (Priority: MEDIUM)
- [ ] JWT токены
- [ ] RBAC (Role-Based Access Control)
- [ ] Сохранение пользовательских отчётов

### 5️⃣ Production (Priority: MEDIUM)
- [ ] SSL/TLS
- [ ] CI/CD pipeline
- [ ] Мониторинг (Sentry, ELK)
- [ ] Database backups

## 🐛 Troubleshooting & FAQ

**Полная документация проблем и решений доступна в файле [`TROUBLESHOOTING.md`](./TROUBLESHOOTING.md)**

### ⚠️ Ошибка: "pip install qwen-api" - пакет не найден?

**Решение**: Используйте `openai` вместо `qwen-api`

```bash
# ❌ Неправильно
pip install qwen-api

# ✅ Правильно  
pip install openai==1.3.0
```

**Подробный гайд**: [`QUICK_FIX_QWEN.md`](./QUICK_FIX_QWEN.md)

---

### Контейнеры не запускаются

```bash
# Проверьте логи
docker-compose logs -f

# Убедитесь, что порты свободны
lsof -i :5173  # Frontend
lsof -i :8000  # Backend
lsof -i :5432  # PostgreSQL
```

### API не отвечает

```bash
# Проверьте статус сервисов
docker-compose ps

# Выполните миграции вручную
docker-compose exec backend python manage.py migrate

# Перезагрузите backend
docker-compose restart backend
```

### Frontend не подключается к backend

```bash
# Проверьте CORS настройки
# backend/config/settings.py - CORS_ALLOWED_ORIGINS

# Проверьте proxy в vite.config.ts
# Убедитесь, что backend запущен: curl http://localhost:8000/api/status/
```

### 🤖 Как установить AI анализ?

**Рекомендуется**: OpenAI GPT-3.5-turbo

```bash
bash backend/setup_llm.sh
# Получить API ключ: https://platform.openai.com/api-keys
# Добавить в .env: OPENAI_API_KEY=sk-...
```

**Подробный гайд**: [`LLM_SETUP.md`](./LLM_SETUP.md)

## 📚 Документация

- [Django](https://docs.djangoproject.com/) - Web framework
- [Django REST Framework](https://www.django-rest-framework.org/) - API toolkit
- [Celery](https://docs.celeryproject.org/) - Task queue
- [React](https://react.dev/) - UI library
- [Vite](https://vitejs.dev/) - Build tool
- [Grafana](https://grafana.com/docs/) - Visualization

## 📝 Лицензия

MIT License - see LICENSE file

## 👥 Contributing

Пуллреквесты приветствуются! Для больших изменений сначала откройте issue.

---

**Создано для Хакатона Сбера** 🎯

- Edit files directly within the Codespace and commit and push your changes once you're done.

## What technologies are used for this project?

This project is built with:

- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS

## How can I deploy this project?

Simply open [Lovable](https://lovable.dev/projects/a9a6dc49-f4f4-4b1e-8f6e-da246b91e2f2) and click on Share -> Publish.

## Can I connect a custom domain to my Lovable project?

Yes, you can!

To connect a domain, navigate to Project > Settings > Domains and click Connect Domain.

Read more here: [Setting up a custom domain](https://docs.lovable.dev/features/custom-domain#custom-domain)
