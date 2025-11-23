# ⚡ Quick Commands Reference

## 🚀 Docker Compose (Recommended - One Command)

```bash
cd backend && cp .env.example .env && docker-compose up -d
```

Then access:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api
- Admin: http://localhost:8000/admin (admin/admin)
- Grafana: http://localhost:3000 (admin/admin)

## 🔍 Verify Everything Works

```bash
# Check API status
curl http://localhost:8000/api/status/

# Get list of banks
curl http://localhost:8000/api/banks/

# Main endpoint - compare banks
curl "http://localhost:8000/api/compare/?banks=sber,vtb&criteria=cost,sms&product=deposits"

# Check running containers
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f celery_worker
```

## 📦 Local Setup (Without Docker)

### Terminal 1: Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py init_data
python manage.py runserver 0.0.0.0:8000
```

### Terminal 2: Celery Worker
```bash
cd backend
source venv/bin/activate
celery -A config worker --loglevel=info
```

### Terminal 3: Celery Beat
```bash
cd backend
source venv/bin/activate
celery -A config beat --loglevel=info
```

### Terminal 4: Frontend
```bash
npm install
npm run dev
```

## 🧹 Cleanup

```bash
# Stop all services
docker-compose down

# Remove all containers and volumes
docker-compose down -v

# Clean frontend build
npm run clean
rm -rf dist/

# Stop local services
Ctrl+C in each terminal
```

## 📊 Database Commands

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U sberbench -d sberbench

# Backup database
docker-compose exec postgres pg_dump -U sberbench sberbench > backup.sql

# Restore database
docker-compose exec -T postgres psql -U sberbench sberbench < backup.sql
```

## 🔧 Django Management

```bash
# Run migrations
docker-compose exec backend python manage.py migrate

# Initialize data
docker-compose exec backend python manage.py init_data

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Shell access
docker-compose exec backend python manage.py shell

# Check static files
docker-compose exec backend python manage.py collectstatic --noinput

# Run tests
docker-compose exec backend python manage.py test
```

## ⏱️ Celery Tasks

```bash
# Run parsing task
docker-compose exec backend celery -A config call apps.tasks.celery_tasks.parse_product_data --args '["deposits", "mock"]'

# Cleanup old snapshots
docker-compose exec backend celery -A config call apps.tasks.celery_tasks.cleanup_old_snapshots --args '[30]'

# Get metrics
docker-compose exec backend celery -A config call apps.tasks.celery_tasks.update_parser_metrics

# Monitor with Flower
docker-compose exec backend pip install flower
docker-compose exec backend celery -A config flower
# Access: http://localhost:5555
```

## 🐛 Debugging

```bash
# View backend logs
docker-compose logs -f backend --tail=50

# View Celery worker logs
docker-compose logs -f celery_worker --tail=50

# Attach to backend container
docker-compose exec backend /bin/bash

# PostgreSQL logs
docker-compose logs -f postgres

# Redis logs
docker-compose logs -f redis
```

## 📝 Code Quality

```bash
# Lint Python (if installed)
cd backend
flake8 apps/

# Format Python
black apps/

# Type check (optional)
mypy apps/

# Lint frontend
npm run lint

# Format frontend
npm run format
```

## 🚀 Deployment Preparation

```bash
# Build frontend for production
npm run build

# Create production settings
cp backend/.env.example backend/.env.production
# Edit backend/.env.production with production values

# Test production Docker build
docker build -f backend/Dockerfile -t sberbench:latest backend/

# Push to registry (if using Docker Hub)
docker tag sberbench:latest yourusername/sberbench:latest
docker push yourusername/sberbench:latest
```

## 📊 API Curl Examples

### Get Status
```bash
curl -X GET http://localhost:8000/api/status/ \
  -H "Content-Type: application/json"
```

### List Banks
```bash
curl -X GET http://localhost:8000/api/banks/ \
  -H "Content-Type: application/json"
```

### Compare Banks
```bash
curl -X GET "http://localhost:8000/api/compare/?banks=sber,vtb,alfa&criteria=cost,sms,interest&product=deposits" \
  -H "Content-Type: application/json"
```

### Get Snapshots
```bash
curl -X GET http://localhost:8000/api/snapshots/ \
  -H "Content-Type: application/json"
```

## 🔑 Environment Variables Quick Setup

```bash
# Create .env for backend
cat > backend/.env << EOF
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production
DB_ENGINE=django.db.backends.postgresql
DB_NAME=sberbench
DB_USER=sberbench
DB_PASSWORD=sberbench
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/0
CORS_ALLOWED_ORIGINS=http://localhost:5173
EOF

# Create .env for frontend
cat > .env << EOF
VITE_API_URL=http://localhost:8000
EOF
```

---

**Quick Reference maintained: 22 Nov 2025**
**For: SberBench Insights - Bank Benchmarking MVP**
