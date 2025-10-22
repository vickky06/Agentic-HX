# Application Layer

## Role
Use cases and application-specific business rules. Orchestrates domain objects to fulfill application requirements.

## What to Add Here
- **Application Services**: Use cases and application workflows
- **DTOs**: Data transfer objects for API communication
- **Application-specific business logic**

## Connections
- **Implements**: Use cases and application workflows
- **Uses**: Domain entities, services, and repository interfaces
- **Used by**: Presentation layer (handlers)
- **Example**: `UserHandler` → `UserService` → `User` entity + `UserRepository`
