#!/bin/bash
# 🚀 Quick LLM Setup Script

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         LLM Integration Setup - OpenAI GPT-3.5            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Install OpenAI package
echo "📦 Step 1: Installing OpenAI package..."
pip install openai==1.3.0
echo "✅ OpenAI installed"
echo ""

# Step 2: Check if .env exists
echo "📝 Step 2: Setting up .env file..."

if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ Created .env from .env.example"
else
    echo "✅ .env file exists"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              NEXT STEPS - Важно!                          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "1️⃣  Получить API ключ:"
echo "   👉 https://platform.openai.com/api-keys"
echo ""
echo "2️⃣  Добавить в .env файл:"
echo "   OPENAI_API_KEY=sk-proj-your-key-here"
echo ""
echo "3️⃣  Готово! Система автоматически будет использовать GPT"
echo ""
echo "💡 Без API ключа система использует mock-анализ (для разработки)"
echo ""
echo "════════════════════════════════════════════════════════════"
echo "Для информации см. LLM_SETUP.md"
echo "════════════════════════════════════════════════════════════"
