## 🚀 Deployment & API Documentation

**Swagger UI (Interactive API Docs):** https://literacy-platform-backend-zapu.onrender.com/docs

**Deployment Link:** https://literacy-platform-backend-zapu.onrender.com/ 

## 🛠 CI Status
[![CI Pipeline](https://github.com/nursayatsailaubekov/literacy-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/nursayatsailaubekov/literacy-platform/actions/workflows/ci.yml)

# Children's Literacy Learning Platform

A production-ready backend API for a Duolingo ABC-like children's literacy learning platform built with FastAPI, PostgreSQL, and SQLAlchemy.

## Features

- **Authentication & Authorization**: JWT-based authentication with role-based access control (Parent, Admin)
- **Child Profiles**: Parents can create and manage multiple child profiles
- **Curriculum Management**: Hierarchical structure of Units → Lessons → Exercises
- **Learning Progress**: Track exercise submissions and lesson completions
- **Gamification**: XP system, level progression, streak tracking, and badge awards
- **Real-time Notifications**: WebSocket-based notifications for badges and achievements
- **RESTful API**: Clean, well-documented API endpoints
- **Database Migrations**: Alembic for database schema versioning
- **Testing**: Comprehensive test suite with pytest

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Testing**: pytest
- **WebSockets**: FastAPI native WebSocket support

## Architecture

The project follows a clean layered architecture:

```
app/
├── core/           # Configuration and security utilities
├── db/             # Database connection
├── models/         # SQLAlchemy models
├── schemas/        # Pydantic schemas for validation
├── repositories/   # Database access layer
├── services/       # Business logic layer
├── api/            # API routes and dependencies
├── websocket/      # WebSocket connection management
└── tests/          # Test suite
```

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL 14+

### Setup Steps

1. **Clone the repository**
   ```bash
   cd literacy_platform
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   ```bash
   # Create database and user
   psql -U postgres
   CREATE DATABASE literacy_db;
   CREATE USER literacy_user WITH PASSWORD 'literacy_pass';
   GRANT ALL PRIVILEGES ON DATABASE literacy_db TO literacy_user;
   \q
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and update settings (especially SECRET_KEY!)
   ```

6. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

7. **Seed initial data (optional)**
   ```bash
   python scripts/seed_data.py
   ```

8. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new parent account
- `POST /api/v1/auth/login` - Login and get JWT tokens
- `GET /api/v1/auth/me` - Get current user information

### Children
- `POST /api/v1/children` - Create a child profile
- `GET /api/v1/children` - Get all children for the current user
- `GET /api/v1/children/{child_id}` - Get a specific child
- `PUT /api/v1/children/{child_id}` - Update a child profile
- `DELETE /api/v1/children/{child_id}` - Delete a child profile

### Curriculum (Admin)
- `POST /api/v1/curriculum/units` - Create a unit
- `GET /api/v1/curriculum/units` - Get all units
- `POST /api/v1/curriculum/lessons` - Create a lesson
- `GET /api/v1/curriculum/units/{unit_id}/lessons` - Get lessons for a unit
- `POST /api/v1/curriculum/exercises` - Create an exercise
- `GET /api/v1/curriculum/lessons/{lesson_id}/exercises` - Get exercises for a lesson

### Learning
- `POST /api/v1/learning/children/{child_id}/exercises` - Submit an exercise answer
- `POST /api/v1/learning/children/{child_id}/lessons/{lesson_id}/complete` - Complete a lesson

### Gamification
- `POST /api/v1/gamification/badges` - Create a badge (admin only)
- `GET /api/v1/gamification/badges` - Get all available badges
- `GET /api/v1/gamification/children/{child_id}/badges` - Get badges earned by a child

### Notifications
- `GET /api/v1/notifications/children/{child_id}` - Get notifications for a child
- `PUT /api/v1/notifications/{notification_id}/read` - Mark notification as read
- `PUT /api/v1/notifications/children/{child_id}/read-all` - Mark all notifications as read

### WebSocket
- `WS /ws/notifications/{child_id}?token={jwt_token}` - Real-time notifications

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest app/tests/test_auth.py
```

## Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

## Development

### Project Structure

```
literacy_platform/
├── alembic/                 # Database migrations
│   └── versions/
├── app/
│   ├── api/
│   │   └── routes/         # API endpoint definitions
│   ├── core/               # Configuration and security
│   ├── db/                 # Database connection
│   ├── models/             # SQLAlchemy ORM models
│   ├── repositories/       # Data access layer
│   ├── schemas/            # Pydantic validation schemas
│   ├── services/           # Business logic
│   ├── tests/              # Test suite
│   ├── websocket/          # WebSocket handlers
│   └── main.py             # FastAPI application
├── scripts/                # Utility scripts
├── .env.example            # Environment variables template
├── alembic.ini             # Alembic configuration
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Python dependencies
└── README.md
```

### Adding New Features

1. **Create models** in `app/models/`
2. **Create schemas** in `app/schemas/`
3. **Create repository** in `app/repositories/`
4. **Implement business logic** in `app/services/`
5. **Add API routes** in `app/api/routes/`
6. **Write tests** in `app/tests/`
7. **Create migration**: `alembic revision --autogenerate -m "Description"`

## Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- Role-based access control (RBAC)
- Parent-child ownership validation
- Admin-only endpoints for curriculum management
- CORS protection

## Production Deployment

1. **Update environment variables**
   - Set `DEBUG=False`
   - Generate a secure `SECRET_KEY` (min 32 characters)
   - Update `DATABASE_URL` with production credentials
   - Configure `CORS_ORIGINS` for your frontend domain

2. **Use a production WSGI server**
   ```bash
   pip install gunicorn
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

3. **Set up a reverse proxy** (nginx, Caddy, etc.)

4. **Enable HTTPS** with SSL certificates

5. **Run migrations** on production database
   ```bash
   alembic upgrade head
   ```

## License

MIT License

## Support

For issues and questions, please open an issue on the GitHub repository.
