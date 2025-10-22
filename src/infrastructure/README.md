# Infrastructure Layer

## Role
External concerns and technical implementations. Implements domain interfaces.

## What to Add Here
- **Database**: Database models, connections, and configurations
- **External APIs**: Third-party service integrations
- **Adapters**: Repository implementations and external service adapters

## Connections
- **Implements**: Domain repository interfaces and external service contracts
- **Used by**: Application layer through dependency injection
- **Uses**: External systems (databases, APIs, file systems)
- **Example**: `UserRepository` (interface) ← `UserRepositoryImpl` (infrastructure)
