# Presentation Layer

## Role
User interface and external communication. Handles HTTP requests and responses.

## What to Add Here
- **API**: FastAPI application setup and configuration
- **Handlers**: HTTP request handlers and routing
- **Dependencies**: Dependency injection configuration

## Connections
- **Implements**: HTTP API endpoints
- **Uses**: Application services through dependency injection
- **Used by**: External clients (web, mobile, API consumers)
- **Example**: HTTP Request → `UserHandler` → `UserService` → Domain
