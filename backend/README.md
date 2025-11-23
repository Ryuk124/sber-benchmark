# Backend Setup and Running

## Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

## Installation (without Docker)

### 1. Create virtual environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create .env file

```bash
cp .env.example .env
```

Edit `.env` and set your configuration:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to False in production
- `DB_*`: PostgreSQL credentials
- `REDIS_URL`: Redis connection string

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Initialize sample data

```bash
python manage.py init_data
```

### 6. Create superuser

```bash
python manage.py createsuperuser
```

### 7. Run development server

```bash
python manage.py runserver 0.0.0.0:8000
```

Visit http://localhost:8000/admin to access Django admin.

### 8. Run Celery worker (in separate terminal)

```bash
celery -A config worker --loglevel=info
```

### 9. Run Celery beat scheduler (in separate terminal)

```bash
celery -A config beat --loglevel=info
```

## Running with Docker Compose

```bash
# Copy example env
cp .env.example .env

# Build and start services
docker-compose up -d

# Initialize data (if not done automatically)
docker-compose exec backend python manage.py init_data

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

## API Endpoints

### Health Check
- `GET /api/status/` - Check API status

### Banks
- `GET /api/banks/` - List all banks
- `GET /api/banks/{id}/` - Get bank details

### Products
- `GET /api/products/` - List all products
- `GET /api/products/{id}/` - Get product details

### Criteria
- `GET /api/criteria/` - List all criteria
- `GET /api/criteria/{id}/` - Get criterion details

### Comparison
- `GET /api/compare/?banks=sber,vtb&criteria=cost,sms&product=deposits` - Compare banks

### Snapshots
- `GET /api/snapshots/` - List all snapshots
- `GET /api/snapshots/{product_id}/` - List snapshots for product

## Testing

```bash
python manage.py test
```

## Admin Panel

Admin interface: http://localhost:8000/admin

Default credentials: See Django superuser setup

## Celery Tasks

### Run parsing task

```bash
celery -A config call apps.tasks.celery_tasks.parse_product_data --args '["deposits", "mock"]'
```

## Development Tips

- Enable debug mode for detailed error messages
- Use `python manage.py shell` for interactive testing
- Check logs in `logs/django.log`
- Use Django admin to manage data

## Project Structure

```
backend/
├── config/                 # Django settings and configuration
├── apps/
│   ├── benchmark/         # Main benchmarking app
│   │   ├── models.py     # Database models
│   │   ├── views.py      # API views
│   │   ├── serializers.py # DRF serializers
│   │   ├── urls.py       # URL routing
│   │   └── admin.py      # Django admin
│   ├── parsers/           # Parser modules
│   │   ├── base.py       # Base parser classes
│   │   └── scrapers/     # Specific scrapers
│   └── tasks/             # Celery tasks
├── manage.py              # Django management
├── requirements.txt       # Python dependencies
└── docker-compose.yml    # Docker services definition
```

## Next Steps

1. Implement specific parsers in `apps/parsers/`
2. Add scheduled tasks in Celery Beat
3. Set up Grafana dashboards
4. Configure monitoring and alerts
5. Integrate with frontend React app
