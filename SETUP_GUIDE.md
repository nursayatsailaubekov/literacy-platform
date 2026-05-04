# Quick Setup Guide

## Prerequisites

- Python 3.11+
- PostgreSQL 14+

## Quick Start

### 1. Set Up PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Run these commands in psql:
CREATE DATABASE literacy_db;
CREATE USER literacy_user WITH PASSWORD 'literacy_pass';
GRANT ALL PRIVILEGES ON DATABASE literacy_db TO literacy_user;
\q
```

### 2. Install and Run

```bash
# Navigate to project directory
cd literacy_platform

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# IMPORTANT: Edit .env and set a secure SECRET_KEY
# You can generate one with: openssl rand -hex 32

# Run database migrations
alembic upgrade head

# Seed initial data (optional but recommended)
python scripts/seed_data.py

# Start the server
uvicorn app.main:app --reload
```

### 3. Access the API

- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Test Credentials (After Seeding)

- **Admin**: admin@literacy.com / Admin123!
- **Parent**: parent@example.com / Parent123!

## Quick Test

### Register a New User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!",
    "full_name": "Test User"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!"
  }'
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html  # On Mac
# Or navigate to htmlcov/index.html in your browser
```

## Common Issues

### Database Connection Error
- Ensure PostgreSQL is running: `sudo service postgresql status`
- Check DATABASE_URL in .env matches your PostgreSQL credentials

### Migration Error
- Reset migrations: `alembic downgrade base`
- Re-run: `alembic upgrade head`

### Import Errors
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

## Next Steps

1. Explore the API documentation at http://localhost:8000/docs
2. Create a parent account and child profile
3. Create curriculum content (requires admin account)
4. Test the learning flow by submitting exercises
5. Check out the gamification features (badges, XP, levels)
6. Test real-time notifications via WebSocket

## Project Structure Overview

```
literacy_platform/
├── app/
│   ├── api/routes/          # API endpoints
│   ├── core/                # Config & security
│   ├── models/              # Database models
│   ├── repositories/        # Data access
│   ├── services/            # Business logic
│   ├── schemas/             # Validation
│   └── tests/               # Test suite
├── alembic/                 # Migrations
├── scripts/                 # Utility scripts
└── requirements.txt         # Dependencies
```

## Development Tips

- Use the interactive docs at /docs to test endpoints
- Check the test files for usage examples
- Review the README.md for detailed documentation
- The seed_data.py script creates sample content for testing
