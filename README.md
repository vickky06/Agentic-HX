# Hexagonal Architecture in Python

A clean implementation of hexagonal architecture (ports and adapters) in Python using FastAPI, SQLAlchemy, and modern Python practices.

## Architecture Overview

This project follows the hexagonal architecture pattern, which separates the core business logic from external concerns like databases, web frameworks, and external APIs.

### Project Structure

```
src/
├── domain/                    # Core business logic
│   ├── entities/             # Domain entities
│   ├── value_objects/        # Value objects
│   ├── services/             # Domain services
│   └── repositories/         # Repository interfaces (ports)
├── application/              # Application layer
│   ├── services/             # Application services (use cases)
│   └── dtos/                 # Data Transfer Objects
├── infrastructure/           # Infrastructure layer
│   ├── database/             # Database implementation
│   ├── external_apis/        # External API integrations
│   └── adapters/             # Infrastructure adapters
└── presentation/             # Presentation layer
    ├── api/                  # API setup
    └── handlers/             # HTTP handlers
```

## Features

- **Clean Architecture**: Separation of concerns with clear boundaries
- **Domain-Driven Design**: Rich domain models with business logic
- **Dependency Injection**: Proper dependency management
- **Async/Await**: Full async support throughout the application
- **Type Safety**: Comprehensive type hints and validation
- **Testing**: Unit, integration, and E2E test structure
- **Database**: PostgreSQL with SQLAlchemy and Alembic migrations
- **API**: FastAPI with automatic OpenAPI documentation

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hexagonal-architecture
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Set up the database:
```bash
# Create PostgreSQL database
createdb hexagonal_db

# Run migrations
uv run alembic upgrade head
```

5. Run the application:
```bash
uv run python main.py
```

The API will be available at `http://localhost:8000` with documentation at `http://localhost:8000/docs`.

## API Endpoints

### Users

- `POST /users/` - Create a new user
- `GET /users/{user_id}` - Get user by ID
- `GET /users/` - Get list of users (with pagination)
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user
- `POST /users/{user_id}/activate` - Activate user
- `POST /users/{user_id}/deactivate` - Deactivate user

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test types
uv run pytest tests/unit/
uv run pytest tests/integration/
uv run pytest tests/e2e/
```

### Code Quality

```bash
# Format code
uv run black src/ tests/

# Sort imports
uv run isort src/ tests/

# Lint code
uv run flake8 src/ tests/

# Type checking
uv run mypy src/
```

### Database Migrations

```bash
# Create a new migration
uv run alembic revision --autogenerate -m "Description"

# Apply migrations
uv run alembic upgrade head

# Rollback migration
uv run alembic downgrade -1
```

## Architecture Principles

### 1. Dependency Inversion
- High-level modules don't depend on low-level modules
- Both depend on abstractions (interfaces)
- Abstractions don't depend on details

### 2. Single Responsibility
- Each class has one reason to change
- Clear separation of concerns

### 3. Open/Closed Principle
- Open for extension, closed for modification
- New features added through new implementations

### 4. Interface Segregation
- Clients shouldn't depend on interfaces they don't use
- Small, focused interfaces

## Key Components

### Domain Layer
- **Entities**: Core business objects with identity
- **Value Objects**: Immutable objects without identity
- **Domain Services**: Business logic that doesn't belong to entities
- **Repository Interfaces**: Contracts for data access

### Application Layer
- **Use Cases**: Application-specific business rules
- **DTOs**: Data transfer objects for API communication

### Infrastructure Layer
- **Repository Implementations**: Concrete data access
- **External Services**: Third-party integrations
- **Database Models**: ORM representations

### Presentation Layer
- **HTTP Handlers**: Request/response handling
- **API Configuration**: FastAPI setup and routing

## Benefits

1. **Testability**: Easy to unit test with mocked dependencies
2. **Maintainability**: Clear separation makes code easier to maintain
3. **Flexibility**: Easy to swap implementations (e.g., database, external APIs)
4. **Scalability**: Well-defined boundaries support team scaling
5. **Independence**: Business logic independent of frameworks and databases

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.
