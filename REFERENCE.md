# 🎯 REFERENCE CARD - Шпаргалка

## 🐛 Ваша ошибка: "pip install qwen-api failed"

```bash
# ❌ Причина
qwen-api пакет не существует в PyPI

# ✅ Решение (выполнить один раз)
pip install openai==1.3.0
```

---

## ⚡ Быстрый старт (3 команды)

```bash
# 1. Backend
cd backend && python manage.py runserver

# 2. Frontend (новый терминал)
npm run dev

# 3. Готово!
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
```

---

## 🤖 Настройка AI (выберите один вариант)

### A) OpenAI GPT-3.5 (рекомендуется) ⭐
```bash
bash backend/setup_llm.sh
# + Получить ключ: https://platform.openai.com/api-keys
# + Добавить в .env: OPENAI_API_KEY=sk-proj-xxxxx
# Стоимость: ~$0.0005/анализ
# Скорость: ⚡ 1-2 сек
```

### B) Ollama LLaMA2 (локально) 🏠
```bash
brew install ollama
ollama run llama2  # в отдельном терминале
# Стоимость: Бесплатно
# Скорость: ⏱️ 10-30 сек
```

### C) Mock-данные (по умолчанию) 🧪
```bash
# Ничего не делать!
# Система уже использует mock
# Стоимость: Бесплатно
# Скорость: ⚡⚡⚡ <100ms
```

---

## 📊 API Endpoints

```bash
# Банки
curl http://localhost:8000/api/banks/

# Продукты
curl http://localhost:8000/api/products/

# Критерии
curl http://localhost:8000/api/criteria/

# Сравнение
curl "http://localhost:8000/api/compare/?banks=sber,vtb"

# AI анализ
curl "http://localhost:8000/api/ai/insights/?banks=sber&product=deposits"

# Django Admin
http://localhost:8000/admin
# Логин: admin / Пароль: admin
```

---

## 📁 Важные файлы

| Путь | Что там | Зачем редактировать |
|------|---------|-------------------|
| `backend/.env` | Переменные окружения | API ключи, БД кредс |
| `backend/requirements.txt` | Python зависимости | Когда нужен новый пакет |
| `src/components/AIInsights.tsx` | React компонент | Если изменить UI |
| `backend/apps/ai/llm_service.py` | LLM логика | Если добавить новый LLM |
| `backend/apps/ai/text_parser.py` | Парсинг сайтов | Если парсить новые источники |

---

## ❌ Проблемы и решения

| Проблема | Решение |
|----------|---------|
| `ModuleNotFoundError: openai` | `pip install openai==1.3.0` |
| `OPENAI_API_KEY not found` | Добавить в `.env` |
| `Invalid API key` | Проверить ключ на https://platform.openai.com/api-keys |
| API не отвечает | `docker-compose ps` → `docker-compose restart backend` |
| Frontend не видит backend | Проверить CORS в `settings.py` |
| Контейнеры не запускаются | `docker-compose logs -f` |
| Database ошибка | `docker-compose exec backend python manage.py migrate` |

**Больше**: см. `TROUBLESHOOTING.md`

---

## 🔄 Docker команды

```bash
# Запустить всё
docker-compose up -d

# Остановить
docker-compose down

# Логи
docker-compose logs -f backend

# Миграции
docker-compose exec backend python manage.py migrate

# Django shell
docker-compose exec backend python manage.py shell

# Перезагрузить
docker-compose restart backend
```

---

## 📚 Документация

- 🆘 Проблемы → `TROUBLESHOOTING.md`
- 🐛 Ваша ошибка → `QUICK_FIX_QWEN.md`
- 🤖 LLM варианты → `LLM_SETUP.md`
- 🚀 Что дальше → `NEXT_STEPS.md`
- 📖 Полная инфа → `README.md`

---

## ✅ Чек-лист: Первый запуск

- [ ] `pip install -r backend/requirements.txt`
- [ ] `cp backend/.env.example backend/.env`
- [ ] Выбрать LLM (A/B/C выше)
- [ ] `python manage.py runserver`
- [ ] `npm run dev` (новый терминал)
- [ ] Открыть http://localhost:5173
- [ ] Выбрать банк и продукт
- [ ] Нажать "Get Insights"
- [ ] Видеть анализ (mock или реальный)

---

## 🎯 Текущее состояние

✅ Backend готов
✅ Frontend готов
✅ Docker готов
✅ Grafana работает
🔄 LLM требует выбора
🔄 Парсеры требуют реализации

---

## 📞 Быстрая помощь

**"Система не запускается"**
```bash
docker-compose restart backend
python manage.py migrate
python manage.py runserver
```

**"AI анализ не работает"**
```bash
# Проверить что установлен openai
python -c "import openai; print(openai.__version__)"

# Если нет:
pip install openai==1.3.0

# Проверить .env
cat backend/.env | grep OPENAI
```

**"Frontend не видит backend"**
```bash
# 1. Проверить что backend работает
curl http://localhost:8000/api/banks/

# 2. Проверить CORS
curl -H "Origin: http://localhost:5173" http://localhost:8000/api/banks/ -v
```

---

**Готово! 🚀 Выполните 3 команды выше и начните работать!**

