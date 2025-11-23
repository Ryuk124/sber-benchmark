#!/bin/bash
# Quick Start - SberBench Insights
# Этот скрипт настроит всю систему за один раз

set -e

echo "🚀 SberBench Insights - Быстрый старт"
echo "======================================="
echo ""

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен"
    echo "📥 Установите Docker: https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose не установлен"
    echo "📥 Установите Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker и Docker Compose установлены"
echo ""

# Переход в backend директорию
cd backend

# Создание .env если не существует
if [ ! -f .env ]; then
    echo "📝 Создание файла .env..."
    cp .env.example .env
    echo "✅ .env создан"
    echo ""
    echo "⚠️  ВАЖНО: Отредактируйте backend/.env перед запуском"
    echo "   (по умолчанию используются значения для разработки)"
fi

echo ""
echo "🐳 Запуск Docker сервисов..."
echo ""

# Запуск Docker Compose
docker-compose up -d

echo ""
echo "⏳ Ожидание инициализации сервисов (30 сек)..."
sleep 30

echo ""
echo "✅ Все сервисы запущены!"
echo ""
echo "📍 Доступные сервисы:"
echo "   • Frontend:      http://localhost:5173"
echo "   • Backend API:   http://localhost:8000/api"
echo "   • Django Admin:  http://localhost:8000/admin (admin/admin)"
echo "   • Grafana:       http://localhost:3000 (admin/admin)"
echo "   • InfluxDB:      http://localhost:8086"
echo ""
echo "📊 Статус сервисов:"
docker-compose ps
echo ""
echo "📚 Документация:"
echo "   • Подробная инструкция: see backend/README.md"
echo "   • Полная архитектура: see FULL_SETUP.md"
echo "   • Интеграция: see INTEGRATION_SUMMARY.md"
echo ""
echo "🛑 Для остановки: docker-compose down"
echo "📋 Для логов: docker-compose logs -f"
echo ""
