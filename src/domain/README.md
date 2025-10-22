# Domain Layer

## Role
Core business logic and rules. Contains the heart of the application - entities, value objects, and business services.

## What to Add Here
- **Entities**: Core business objects with identity (e.g., `User`, `Order`, `Product`)
- **Value Objects**: Immutable objects without identity (e.g., `Email`, `Money`, `Address`)
- **Domain Services**: Business logic that doesn't belong to entities
- **Repository Interfaces**: Contracts for data access (ports)

## Connections
- **Implements**: Nothing (pure business logic)
- **Implemented by**: Application layer uses domain entities and services
- **Called by**: Application services call domain services and repositories
- **Example**: `UserService` (application) → `UserDomainService` (domain) → `UserRepository` (interface)
