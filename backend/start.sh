#!/bin/bash

# Quick Start Script for SberBench Insights

set -e

echo "🚀 SberBench Insights - Quick Start"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    echo "Please install Docker from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed${NC}"
    echo "Please install Docker Compose from: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✓ Docker and Docker Compose are installed${NC}"
echo ""

# Navigate to backend directory
cd backend

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}📝 Creating .env file from .env.example${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env created${NC}"
fi

echo ""
echo -e "${YELLOW}🐳 Starting Docker services...${NC}"
echo ""

# Start services
docker-compose up -d

echo ""
echo -e "${GREEN}✓ All services are starting...${NC}"
echo ""

# Wait for services to be ready
echo -e "${YELLOW}⏳ Waiting for services to be healthy...${NC}"
sleep 10

# Run migrations and init data
echo -e "${YELLOW}🗄️  Running database migrations...${NC}"
docker-compose exec -T backend python manage.py migrate || true

echo -e "${YELLOW}📊 Initializing sample data...${NC}"
docker-compose exec -T backend python manage.py init_data || true

echo ""
echo -e "${GREEN}✓ Setup completed!${NC}"
echo ""
echo "📍 You can now access:"
echo ""
echo -e "${GREEN}Frontend:${NC}        http://localhost:5173"
echo -e "${GREEN}Backend API:${NC}     http://localhost:8000/api"
echo -e "${GREEN}Django Admin:${NC}    http://localhost:8000/admin"
echo -e "${GREEN}Grafana:${NC}        http://localhost:3000 (admin/admin)"
echo ""
echo "📚 Next steps:"
echo "  1. Open http://localhost:5173 in your browser"
echo "  2. Start using the benchmarking system"
echo "  3. Check backend/README.md for more details"
echo ""
echo "🛑 To stop all services: docker-compose down"
echo "📋 To view logs: docker-compose logs -f"
echo ""
