# Zero Trust Network Platform

A production-grade Zero Trust cybersecurity platform built with Python, FastAPI, PostgreSQL, Redis, Docker, and Clean Architecture principles.

## Features

- **Clean Architecture**: Domain-driven design with clear separation of concerns
- **Zero Trust Security**: Continuous validation of identity, device, and behavior posture
- **Multi-layer Authentication**: MFA support, device trust evaluation, risk-based access control
- **Scalable Infrastructure**: Docker containerization with PostgreSQL and Redis
- **Comprehensive Logging**: Structured logging with JSON/text format support
- **Testing Framework**: Unit, integration, and E2E tests with pytest
- **CI/CD Pipeline**: GitHub Actions for automated testing and deployment
- **Monitoring**: Prometheus metrics and Grafana dashboards

## Architecture

The platform follows Clean Architecture principles with three main layers:

- **Domain Layer**: Business entities, value objects, repositories interfaces, and domain services
- **Application Layer**: Use cases, DTOs, and application interfaces
- **Infrastructure Layer**: Database implementations, external services, and messaging

## Project Structure

```
ztn/
├── apps/
│   ├── api/              # FastAPI application
│   │   ├── api/         # API endpoints
│   │   ├── config/      # Configuration management
│   │   └── core/        # Core utilities (logging, dependencies)
│   └── worker/          # Celery background workers
├── src/
│   ├── domain/          # Domain layer
│   │   ├── entities/    # Business entities
│   │   ├── value_objects/  # Value objects
│   │   ├── repositories/   # Repository interfaces
│   │   └── services/    # Domain services
│   ├── application/     # Application layer
│   │   ├── use_cases/   # Business use cases
│   │   ├── dto/         # Data transfer objects
│   │   └── interfaces/  # Application interfaces
│   └── infrastructure/  # Infrastructure layer
│       ├── persistence/ # Database implementations
│       │   ├── postgresql/
│       │   └── redis/
│       ├── external_services/
│       └── messaging/
├── tests/
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── e2e/             # End-to-end tests
├── scripts/
│   ├── deployment/      # Deployment scripts
│   └── migration/       # Database migrations
├── .github/
│   └── workflows/       # CI/CD pipelines
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL 15+
- Redis 7+

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd ztn
```

2. **Install dependencies**
```bash
pip install -e ".[dev]"
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Start services with Docker Compose**
```bash
docker-compose up -d
```

5. **Run database migrations**
```bash
# Apply initial schema
psql -h localhost -U ztn -d ztn_db -f scripts/migration/init.sql
```

6. **Start the API server**
```bash
uvicorn apps.api.main:app --reload
```

### Running Tests

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit

# Run integration tests only
pytest tests/integration

# Run with coverage
pytest --cov=apps --cov=src --cov-report=html
```

### Code Quality

```bash
# Format code
black apps src tests

# Lint code
ruff check apps src tests

# Type checking
mypy apps src tests
```

## Configuration

Configuration is managed through environment variables and Pydantic Settings. Key configuration options:

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: JWT signing secret
- `ENVIRONMENT`: Environment (development/production)
- `DEBUG`: Enable debug mode
- `LOG_LEVEL`: Logging level (DEBUG/INFO/WARNING/ERROR/CRITICAL)
- `LOG_FORMAT`: Log format (json/text)

## Deployment

### Docker Deployment

Build and run with Docker Compose:

```bash
docker-compose up -d
```

### Manual Deployment

1. Build the Docker image:
```bash
docker build -t ztn-platform .
```

2. Run the container:
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql+asyncpg://... \
  -e REDIS_URL=redis://... \
  ztn-platform
```

### CI/CD

The project includes GitHub Actions workflows for:

- **CI**: Linting, testing, and security scanning on every push
- **CD**: Automated Docker image building and deployment on main branch
- **Dependency Review**: Automated dependency vulnerability scanning

## API Documentation

When running in development mode, API documentation is available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Monitoring

- **Prometheus**: `http://localhost:9090`
- **Grafana**: `http://localhost:3000` (admin/admin)
- **Metrics Endpoint**: `http://localhost:8000/metrics`

## Security Features

- Multi-factor authentication (MFA)
- Device trust evaluation
- Risk-based access control
- Account lockout after failed attempts
- Session timeout management
- Rate limiting
- CORS protection
- Trusted host middleware

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Support

For issues and questions, please open an issue on GitHub.
