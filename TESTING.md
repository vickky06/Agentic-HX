# Testing Guide for Hexagonal Architecture

This guide covers different ways to test the hexagonal architecture application.

## 🧪 **Types of Testing**

### 1. **Unit Tests** (Automated)
Test individual components in isolation.

```bash
# Run all unit tests
uv run pytest tests/unit/ -v

# Run specific test file
uv run pytest tests/unit/test_email_value_object.py -v

# Run with coverage
uv run pytest tests/unit/ --cov=src --cov-report=html
```

### 2. **Integration Tests** (Automated)
Test component interactions.

```bash
# Run integration tests
uv run pytest tests/integration/ -v

# Run all tests
uv run pytest tests/ -v
```

### 3. **Manual Testing** (Interactive)
Test components manually without database.

```bash
# Run manual tests
uv run python test_manual.py
```

### 4. **API Testing** (Interactive)
Test the running application via HTTP.

```bash
# Start the application
uv run python main.py

# In another terminal, run API tests
uv run python test_api.py
```

## 🚀 **Quick Start Testing**

### Step 1: Run Unit Tests
```bash
uv run pytest tests/unit/ -v
```

### Step 2: Run Manual Tests
```bash
uv run python test_manual.py
```

### Step 3: Test the API (Optional - requires database setup)
```bash
# Terminal 1: Start the app
uv run python main.py

# Terminal 2: Test the API
uv run python test_api.py
```

## 🔧 **Testing with Database**

To test with a real database:

### 1. Set up PostgreSQL
```bash
# Install PostgreSQL (if not already installed)
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql

# Start PostgreSQL
# macOS: brew services start postgresql
# Ubuntu: sudo systemctl start postgresql

# Create database
createdb hexagonal_db
```

### 2. Configure Environment
```bash
# Copy environment file
cp .env.example .env

# Edit .env with your database credentials
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=hexagonal_db
# DB_USER=your_username
# DB_PASSWORD=your_password
```

### 3. Run Migrations
```bash
uv run alembic upgrade head
```

### 4. Start and Test
```bash
# Start the application
uv run python main.py

# Test the API
uv run python test_api.py
```

## 📊 **Testing Commands Reference**

### Pytest Commands
```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/unit/test_user_entity.py

# Run tests matching pattern
uv run pytest -k "test_email"

# Run with coverage
uv run pytest --cov=src

# Run with coverage and HTML report
uv run pytest --cov=src --cov-report=html

# Run only unit tests
uv run pytest tests/unit/

# Run only integration tests
uv run pytest tests/integration/

# Run with specific markers
uv run pytest -m unit
uv run pytest -m integration
```

### Manual Testing
```bash
# Test domain layer
uv run python test_manual.py

# Test specific components
uv run python -c "
from src.domain.entities.user import User
from src.domain.value_objects.email import Email
email = Email.from_string('test@example.com')
user = User(email=email, first_name='John', last_name='Doe')
print(f'User created: {user}')
"
```

### API Testing
```bash
# Test with curl
curl http://localhost:8000/health
curl http://localhost:8000/

# Test user creation
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "first_name": "John", "last_name": "Doe"}'

# Test user list
curl http://localhost:8000/users/
```

## 🎯 **What Each Test Covers**

### Unit Tests
- ✅ Email value object validation
- ✅ User entity business logic
- ✅ Domain services
- ✅ Value object equality and hashing

### Integration Tests
- ✅ Application services with mocked dependencies
- ✅ Repository implementations
- ✅ Service interactions

### Manual Tests
- ✅ Domain entities creation and methods
- ✅ Value object validation
- ✅ Application DTOs
- ✅ Infrastructure configuration
- ✅ FastAPI app creation

### API Tests
- ✅ HTTP endpoints
- ✅ Request/response handling
- ✅ Error handling
- ✅ Full application workflow

## 🐛 **Troubleshooting**

### Common Issues

1. **Database Connection Errors**
   - Ensure PostgreSQL is running
   - Check database credentials in `.env`
   - Verify database exists

2. **Import Errors**
   - Run `uv sync` to install dependencies
   - Check Python path

3. **Test Failures**
   - Check test output for specific error messages
   - Ensure all dependencies are installed
   - Verify test data is valid

### Debug Mode
```bash
# Run tests with debug output
uv run pytest -v -s

# Run with pdb debugger
uv run pytest --pdb

# Run specific test with debug
uv run pytest tests/unit/test_email_value_object.py::TestEmailValueObject::test_create_valid_email -v -s
```

## 📈 **Coverage Reports**

Generate coverage reports to see which code is tested:

```bash
# Generate HTML coverage report
uv run pytest --cov=src --cov-report=html

# Open coverage report
open htmlcov/index.html
```

## 🔄 **Continuous Testing**

For development, you can run tests automatically:

```bash
# Watch for file changes and run tests
uv run pytest-watch

# Or use pytest-xdist for parallel testing
uv run pytest -n auto
```
